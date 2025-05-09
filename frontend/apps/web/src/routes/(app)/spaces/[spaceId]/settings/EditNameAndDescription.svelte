<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import { Button, Input } from "@intric/ui";
  import { Settings } from "$lib/components/layout";

  const spaces = getSpacesManager();
  const currentSpace = spaces.state.currentSpace;

  let currentName = "";
  let currentDescription = "";

  function watch(space: { name: string; description: string | null }) {
    currentName = space.name;
    currentDescription = space.description ?? "";
  }

  $: watch($currentSpace);
</script>

<Settings.Row
  title="Name"
  description="A name to identify this space across your organisation."
  let:labelId
  let:descriptionId
>
  <Input.Text
    class="peer"
    labelClass="text-2xl"
    bind:value={currentName}
    aria-labelledby={labelId}
    aria-describedby={descriptionId}
  ></Input.Text>
  <div
    class="flex h-0 flex-row-reverse items-center justify-between overflow-hidden opacity-0 transition-all duration-300 peer-focus-within:h-12 peer-focus-within:opacity-100"
  >
    <Button
      type="submit"
      variant="primary"
      on:click={() => {
        spaces.updateSpace({ name: currentName });
      }}>Save changes</Button
    >
    <Button
      variant="outlined"
      on:click={() => {
        currentName = $currentSpace.name;
      }}>Revert changes</Button
    >
  </div>
</Settings.Row>

<Settings.Row
  title="Description"
  description="A brief description of this space that will be displayed to its users."
  let:labelId
  let:descriptionId
>
  <Input.TextArea
    bind:value={currentDescription}
    class="peer"
    aria-labelledby={labelId}
    aria-describedby={descriptionId}
  ></Input.TextArea>
  <div
    class="flex h-0 items-center justify-between overflow-hidden opacity-0 transition-all duration-300 peer-focus-within:h-12 peer-focus-within:opacity-100"
  >
    <Button
      variant="outlined"
      on:click={() => {
        currentDescription = $currentSpace.description ?? "";
      }}>Revert changes</Button
    >
    <Button
      variant="primary"
      on:click={() => {
        spaces.updateSpace({ description: currentDescription });
      }}>Save changes</Button
    >
  </div>
</Settings.Row>
