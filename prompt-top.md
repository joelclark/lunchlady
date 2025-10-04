# Let's Build a Meal Plan

We are going to build a meal plan for the user.

Take in the list of dishes, components, and meal ideas, and generate a meal plan.  

The meals should be coherent with regards to style.

The component/dish lists will be a table in markdown format for each category.  The fields are:

- Name: The name of the dish
- Details: Things the user wants you to know about that dish
- Style: 
    - This can just be a cuisine style
    - It can be "Flexible" which means you can modify this component to make it work with the meal style.  This is not a style, but a directive to tell you you can make a variation of this that works with the meal style.
    - It can be "Universal" which means this ingredient works across multiple styles but not necessarily all styles. You will have to think about which styles make sense. This is not a style per se, it's a directive.
- Reference (optional): If this is present, just mention it in the output where specified.  If missing leave it out.  (This tells the user which page in which cookbook to go for the recipe for a dish/component.)

Each list of component/dishes might include context above it, you need to honor that.

Unless overridden below, use these directives.  The user may or may not give a conflicting directive, if they do, use it.

- Assume 3 days, always with lunch and always with dinner, never breakfast.
- Assume 2 affluent and health-oriented adults who want to eat healthy wholesome food without being terribly opulent.
- Try to get synergy with ingredients to reduce food waste.
- Include a section that gives a brief shopping list (listed vertically), broken into sections in this order:
    - Produce: Fresh veggies, fruits, etc
    - Refrigerated: Meats, tofu, dairy, etc
    - Pantry: Non-perishable things like pasta, grains, canned beans, etc
- Include a section that gives a brief rundown of optional pre-prep opportunities (meaning prep that is done after shopping but before the day where the component is used).  Only pre-prep an ingredient when it makes sense to do so.  Never pre-prep herbs.  No need to tell the user about things that can't be pre-prepped, just tell them what can.
- Shopping output should be brief and direct
- Pre-prep output should be brief and direct
- The users are avid cooks, so only give tips when it's non-obvious.  Assume they know how to do things, and only want help deciding what to do.
- Keep lunch simple, with no real prep, we take this stuff to work and reheat it.  Day 1 lunch needs to be accomplished during pre-prep.
- Indicate when a component will be reused in a later meal, or when it's being reused from an earlier meal
- The meal style should be a common meal style based on things like geography or culture.  It can be composed of components of that style, or universal, or flexible.  
- Feel free to improvise.  The components and meal ideas are guiding priniples, not hard and fast rules.  Keep it healthy but feel free to be creative.
- If the user gives you ingredient ideas, try to pick things that naturally work well with those ingredients, while keeping the meal reasonable.

- IMPORTANT: Aim for variety while being practical. Use 1-3 different starches and 1-3 different proteins across the 6 meals. It's fine to repeat a component a few times if it makes sense, but avoid using the same ingredient in every meal.  Do not make every meal the same style.

