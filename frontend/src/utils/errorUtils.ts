/** Converts an unknown thrown value to a human-readable error message string. */
export function toErrorMessage(e: unknown): string {
  return e instanceof Error ? e.message : String(e)
}
