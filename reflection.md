# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design. 
    -    My initial UML design includes my main classes, including their attributes and methods. I have identified four main classes: User, Pet, Task, and Schedule. Users will be able to specify their own preferences, which will help with identifying constraints later when developing schedules. They will also be able to specify their pets' traits. Users should also be able to schedule tasks, and lastly, create a daily schedule along with explanations. 
- What classes did you include, and what responsibilities did you assign to each?
    - I included the User, Pet, Task, and Schedule classes. The User class should store all of the users' characteristics, such as their preferences and availabilities. The Pet should include the pets' needs, such as their hunger and energy. The Tasks would include things like walking and feeding, and would be used by the User to keep track of and fulfill their Pets' needs. Lastly, the User would be able to generate a daily Schedule that includes all of the tasks for a specific pet. 

**b. Design changes**

- Did your design change during implementation?
    - Yes, they did. I asked Copilot to describe any missing relationships, as well as to name certain attributes that would most likely not be used at runtime. Based on Chat's suggestions, I added/changed certain relationships for the classes so that the attributes would actually be used in the program. 
- If yes, describe at least one change and why you made it.
    - One of the changes concerned the "Date" attribute in the Schedule class I created. Originally, the date was not used at all in the relationship between classes, making it a redundant attribute. After consulting Copilot, I decided to make it so that each Schedule had to be linked back to a User. This way, the User can refer back to previous schedules using the Date attribute. 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
    - My scheduler made a tradeoff between efficiency and readability. Originally, my filter_tasks method conducted step-by-step list reassignment. Instead of doing this, the AI suggested I do a one-pass filter to make it faster. However, the tradeoff is that it the code has become a little harder to read for human readers because of the boolean conditions used. 
- Why is that tradeoff reasonable for this scenario?
    - The tradeoff is reasonable because there is still documentation for the methods, which will help future programmers understand what the code does. Furthermore, it is important for the filtering method to be fast in the case that the schedule has a lot of tasks. 

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
    - I used AI tools for creating the UML, implementing main functionalities, and suggesting changes. I primarily used it to suggest algorithmic improvements for the sorting and filtering functionalities. 
- What kinds of prompts or questions were most helpful?
    - Prompts that identified weak spots and suggested improvements were the most helpful, in my opinion. As I did in previous projects, I also asked questions about functionality that was implemented by the AI, which was also very helpful in understanding the changes I was making. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
    - One moment I did not accept an AI suggestion as-is was when I asked it to make my classes a little more related so that there were not just random attributes lying around not being used. The AI wanted to create additional functionalities that I determined were outside the scope of the project, so I did not accept the suggestion. 
- How did you evaluate or verify what the AI suggested?
    - I went back to my original UML design and decided, based on my original goals, how much I was willing to extend outside of the scope of the project. Eventually, I decided to only implement the changes that seemed most necessary for the app to function.  

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
    - I tested several behaviors, such as the sorting and filtering functionalities. I also tested the creation of my four classes and the relationships between them. 
- Why were these tests important?
    - These tests were important because the functionality of the app depended on the functionality of the individual classes. The relationship between them (Users creating Pets, Tasks assigned to Pets) were also crucial to the app working as it should. 

**b. Confidence**

- How confident are you that your scheduler works correctly?
    - I am pretty confident, after the test cases, that my scheduler works correctly. I also used the UI and played around with different scenarios to test it. 
- What edge cases would you test next if you had more time?
    - If I had more time, I would test more scenarios with the scheduler and with pet traits. For example, with the scheduler, I would implement boundaries for weird times that the User wants to schedule tasks. It might not be such a good idea for a user to schedule a walk at midnight. As for Pet traits, I would make sure that there are boundaries for hunger and energy so that the pets' needs are not under or overmet. 

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
    - I am most satisfied with the overall functionality and the cleanliness of the classes with this project. It was a lot of fun generating the mermaid.js diagram, since I have never done something like that before. The diagram really helped me understand how all of the classes I was making would eventually be used to fulfill the project's functionalities. 

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
    - If I had another iteration, I would improve the UI of the project. Looking at the Streamlit app, I think it would be nice if the schedule was able to be viewed in a more accessible and understandable manner, like a calendar view. 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
    - One important thing I learned about designing systems is to keep in mind an original UML design so that you do not lose sight of your original goals. Although changes mid-project are definitely to be expected, it is also crucial that you do not go overboard with adding features, nor do you stray too far from your original intentions. Having my mermaid diagram set aside really helped me focus on core functionality. 