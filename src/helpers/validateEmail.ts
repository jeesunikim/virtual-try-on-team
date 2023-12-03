const EMAIL_FORMAT =
  /^[a-z0-9]+([-._][a-z0-9]+)*(\+[^@]+)?@[a-z0-9]+([.-][a-z0-9]+)*\.[a-z]{2,}$/i;
const MICROSOFT_EMAIL_FORMAT =
  /^[a-z0-9][a-z0-9._-]*[a-z0-9_-]+(\+[a-z0-9]+)?@(hotmail|outlook).com$/i;

export function validateEmail(email: string): boolean {
  return Boolean(
    email.match(EMAIL_FORMAT) || email.match(MICROSOFT_EMAIL_FORMAT)
  );
}
