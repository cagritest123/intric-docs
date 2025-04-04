import { createIntric } from "./src/intric";
export { createIntric } from "./src/intric";
import { createIntricSocket } from "./src/socket/socket";
export { createIntricSocket } from "./src/socket/socket";
export { createClient, IntricError } from "./src/client/client";
export { JSONRequestBody } from "./src/types/fetch";
export * from "./src/types/resources";
export * from "./src/socket/types";
export type Intric = ReturnType<typeof createIntric>;
export type IntricSocket = ReturnType<typeof createIntricSocket>;
