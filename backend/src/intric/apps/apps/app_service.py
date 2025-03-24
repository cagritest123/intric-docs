from typing import TYPE_CHECKING, Optional
from uuid import UUID

from intric.ai_models.completion_models.completion_model import ModelKwargs
from intric.ai_models.completion_models.completion_service import (
    CompletionServiceFactory,
)
from intric.apps.apps.api.app_models import InputField, InputFieldType
from intric.apps.apps.app import App
from intric.apps.apps.app_factory import AppFactory
from intric.apps.apps.app_repo import AppRepository
from intric.files.file_service import FileService
from intric.files.transcriber import Transcriber
from intric.main.exceptions import BadRequestException, UnauthorizedException
from intric.main.models import ModelId
from intric.prompts.prompt_service import PromptService
from intric.spaces.api.space_models import WizardType
from intric.spaces.space import Space
from intric.users.user import UserInDB

if TYPE_CHECKING:
    from intric.actors import ActorManager
    from intric.ai_models.completion_models.completion_model import CompletionModel
    from intric.completion_models.application import CompletionModelCRUDService
    from intric.groups.group_service import GroupService
    from intric.prompts.prompt import Prompt
    from intric.spaces.api.space_models import TemplateCreate
    from intric.spaces.space_repo import SpaceRepository
    from intric.templates.app_template.app_template_service import AppTemplateService


class AppService:
    def __init__(
        self,
        user: UserInDB,
        repo: AppRepository,
        space_repo: "SpaceRepository",
        factory: AppFactory,
        completion_model_crud_service: "CompletionModelCRUDService",
        file_service: FileService,
        prompt_service: PromptService,
        completion_service_factory: CompletionServiceFactory,
        transcriber: Transcriber,
        app_template_service: "AppTemplateService",
        group_service: "GroupService",
        actor_manager: "ActorManager",
    ):
        self.user = user
        self.repo = repo
        self.space_repo = space_repo
        self.factory = factory
        self.completion_model_crud_service = completion_model_crud_service
        self.file_service = file_service
        self.prompt_service = prompt_service
        self.completion_service_factory = completion_service_factory
        self.transcriber = transcriber
        self.app_template_service = app_template_service
        self.group_service = group_service
        self.actor_manager = actor_manager

    async def create_app(
        self, name: str, space: Space, template_data: Optional["TemplateCreate"] = None
    ) -> App:
        actor = self.actor_manager.get_space_actor_from_space(space=space)

        if not actor.can_create_apps():
            raise UnauthorizedException()

        completion_model = await self.get_completion_model(space=space)

        if not template_data:
            app = self.factory.create_app(
                user=self.user,
                space=space,
                name=name,
                completion_model=completion_model,
            )
            app_in_db = await self.repo.add(app)
        else:
            app_in_db = await self._create_from_template(
                space=space,
                template_data=template_data,
                name=name,
                completion_model=completion_model,
            )

        # TODO: Review how we get the permissions to the presentation layer
        permissions = actor.get_app_permissions()

        return app_in_db, permissions

    async def _create_from_template(
        self,
        space: "Space",
        template_data: "TemplateCreate",
        completion_model: "CompletionModel",
        name: str | None = None,
    ):
        template = await self.app_template_service.get_app_template(
            app_template_id=template_data.id
        )

        # Validate incoming data
        template.validate_wizard_data(template_data=template_data)

        attachments = await self.file_service.get_file_infos(
            file_ids=template_data.get_ids_by_type(wizard_type=WizardType.attachments)
        )

        prompt = None
        if template.prompt_text:
            prompt = await self.prompt_service.create_prompt(text=template.prompt_text)

        input_fields = [
            InputField(
                type=InputFieldType(template.input_type),
                description=template.input_description,
            )
        ]

        app = self.factory.create_app_from_template(
            user=self.user,
            template=template,
            name=name or template.name,
            prompt=prompt,
            attachments=attachments,
            completion_model=completion_model,
            input_fields=input_fields,
            space=space,
        )

        return await self.repo.add(app)

    async def get_completion_model(self, space: Space) -> "CompletionModel":
        completion_model = space.get_default_model() or (
            space.get_latest_completion_model()
            if not space.is_personal()
            else await self.completion_model_crud_service.get_default_completion_model()
        )

        if completion_model is None:
            raise BadRequestException()

        return completion_model

    async def get_app(self, app_id: UUID) -> App:
        space = await self.space_repo.get_space_by_app(app_id=app_id)
        app = space.get_app(app_id=app_id)
        actor = self.actor_manager.get_space_actor_from_space(space)

        if not actor.can_read_apps():
            raise UnauthorizedException()

        # TODO: Review how we get the permissions to the presentation layer
        permissions = actor.get_app_permissions()

        return app, permissions

    async def update_app(
        self,
        app_id: UUID,
        name: str | None = None,
        description: str | None = None,
        completion_model_id: UUID | None = None,
        completion_model_kwargs: ModelKwargs | None = None,
        input_fields: list[InputField] | None = None,
        attachment_ids: list[ModelId] | None = None,
        prompt_text: str | None = None,
        prompt_description: str | None = None,
    ) -> App:
        space = await self.space_repo.get_space_by_app(app_id=app_id)
        app = space.get_app(app_id=app_id)
        actor = self.actor_manager.get_space_actor_from_space(space)

        if not actor.can_edit_apps():
            raise UnauthorizedException()

        completion_model = None
        if completion_model_id is not None:
            if not space.is_completion_model_in_space(
                completion_model_id=completion_model_id
            ):
                raise BadRequestException(
                    "The completion model is not enabled in the space."
                )

            else:
                completion_model = (
                    await self.completion_model_crud_service.get_completion_model(
                        completion_model_id
                    )
                )

        attachments = None
        if attachment_ids is not None:
            attachments = await self.file_service.get_file_infos(
                [attachment.id for attachment in attachment_ids]
            )

        prompt = None
        if prompt_text is not None:
            prompt = await self.prompt_service.create_prompt(
                text=prompt_text, description=prompt_description
            )

        app.update(
            name=name,
            description=description,
            completion_model=completion_model,
            completion_model_kwargs=completion_model_kwargs,
            input_fields=input_fields,
            attachments=attachments,
            prompt=prompt,
        )

        app_in_db = await self.repo.update(app)

        # TODO: Review how we get the permissions to the presentation layer
        permissions = actor.get_app_permissions()

        return app_in_db, permissions

    async def delete_app(self, app_id: UUID):
        space = await self.space_repo.get_space_by_app(app_id=app_id)
        actor = self.actor_manager.get_space_actor_from_space(space)

        if not actor.can_delete_apps():
            raise UnauthorizedException()

        await self.repo.delete(app_id)

    async def run_app(self, app_id: UUID, file_ids: list[UUID], text: str | None):
        space = await self.space_repo.get_space_by_app(app_id=app_id)
        app = space.get_app(app_id=app_id)
        actor = self.actor_manager.get_space_actor_from_space(space)

        if not actor.can_read_app(app=app):
            raise UnauthorizedException()

        files = await self.file_service.get_files_by_ids(file_ids=file_ids)

        completion_service = self.completion_service_factory.create_completion_service(
            app.completion_model
        )

        return await app.run(
            files=files,
            text=text,
            completion_service=completion_service,
            transcriber=self.transcriber,
        )

    async def get_prompts_by_app(self, app_id: UUID) -> list["Prompt"]:
        space = await self.space_repo.get_space_by_app(app_id=app_id)
        actor = self.actor_manager.get_space_actor_from_space(space)

        if not actor.can_read_prompts_of_apps():
            raise UnauthorizedException()

        return await self.prompt_service.get_prompts_by_app(app_id=app_id)
