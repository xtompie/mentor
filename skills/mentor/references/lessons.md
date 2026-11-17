# Lessons

A lesson is for the user, not the model. It names an idea the user met in this session and makes it easy to remember and look up.

## Shape

- **Name**: the common term if one exists, so the user can search it. Example: "separate construction from use", "leaky abstraction".
- **What and why**: two or three plain sentences.
- **Here**: the place in this session where it showed up: file, class, turn.
- **For the model** (optional): one line the user can paste next time.

## Example

From a code review where the user explained two things:

1. **Separate construction from use.** Building objects and using them are two jobs. Put building in a factory, so the class that does the work gets ready objects. Here: `OrderService` built a `PdfRenderer` and a `Mailer` inside `send()`.
2. **Leaky abstraction.** A module should return its own types. If module X uses module Y inside and returns Y's result, everyone who calls X now depends on Y too. Here: `Billing::charge()` returned `Stripe\Charge` instead of a `Billing` result.

## Do not

- Write essays unasked. Offer "explain more".
- Invent a lesson the session does not show.
- Lecture about the model's mistakes. Lessons are about the craft and the project.
