**Output Guidance**:

The output should be structured in valid HTML suitable for email clients as follows, with nothing following it. This will go into an email so no further interaction is possible. Items inside {} are directives that are meant for you to interpret and fill in, do not output the { or } in that case.

Use inline CSS styles for compatibility with email clients. Keep styling simple and clean.

Output:


<h1 style="color: #333; font-family: Arial, sans-serif;">Meal Plan</h1>

<h2 style="color: #555; font-family: Arial, sans-serif; margin-top: 20px;">Day N</h2>

<h3 style="color: #666; font-family: Arial, sans-serif; margin-top: 15px;">{Lunch, Dinner etc}: {Brief Title} <span style="font-weight: normal;">({style of meal in parenthesis here})</span></h3>

<ul style="font-family: Arial, sans-serif; line-height: 1.6;">
  <li>{meal components, one bullet per line, add context only if needed, add reference in parens if specified, do not mention style here}</li>
</ul>

<p style="font-family: Arial, sans-serif; font-style: italic; color: #666; margin-top: 10px;">{optional text with any needed meal context, in italics, only if needed}</p>

<h2 style="color: #555; font-family: Arial, sans-serif; margin-top: 20px;">Shopping</h2>

<p style="font-family: Arial, sans-serif; line-height: 1.6;">{shopping output here, optional amounts as needed}</p>

<h2 style="color: #555; font-family: Arial, sans-serif; margin-top: 20px;">Pre-Prep</h2>

<p style="font-family: Arial, sans-serif; line-height: 1.6;">{post shopping prep here}</p>
