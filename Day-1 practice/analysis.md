# Comparing a Plain Chatbot, Rule-Based Workflow, and AI Agent

## 1. Scenario

The scenario chosen for this task is College Event Registration.

The private event data used in the system is:

| Event | Registration Fee | Capacity |
|---|---:|---:|
| TECHFEST2026 | ₹500 | 100 |
| HACKATHON2026 | ₹300 | 50 |
| AIWORKSHOP2026 | ₹200 | 30 |

The systems were tested using the following questions:

1. What is the registration fee for TECHFEST2026?
2. What is the total cost of TECHFEST2026 and AIWORKSHOP2026 after a 10% discount?
3. Is TECHFEST2026 more expensive than AIWORKSHOP2026? If yes, by how much?
4. Give me a two-line welcome message for the college events.

---

## 2. Plain Chatbot

The plain chatbot uses the Groq LLM to generate responses. It does not directly access the private event data stored in the Python program.

For the first question, the chatbot could not provide the TECHFEST2026 registration fee and asked for the price information.

For the second question, it asked for the original prices instead of calculating the answer.

For the third question, it stated that it did not have the cost details and could not compare the events.

For the fourth question, it successfully generated a two-line welcome message.

This shows that a plain chatbot can generate natural-language responses, but it does not automatically have access to private application data.

---

## 3. Rule-Based Workflow

The rule-based workflow uses predefined conditions and Python logic. It does not use an LLM.

The workflow successfully answered all four predefined questions.

It retrieved the TECHFEST2026 fee as ₹500, calculated the combined cost of TECHFEST2026 and AIWORKSHOP2026 as ₹700, applied the 10% discount and obtained ₹630, and calculated the difference between the two event fees as ₹300.

It also returned a predefined welcome message.

The main limitation is that the workflow depends on predefined rules. If a user asks a question in an unexpected format, the corresponding rule may not match the question.

---

## 4. AI Agent

The AI agent combines an LLM with tools and a loop.

Two tools were created:

1. `get_event_fee` - retrieves the registration fee of an event.
2. `calculate` - performs mathematical calculations.

For the TECHFEST2026 fee question, the agent called `get_event_fee`.

For the discount question, the agent called `get_event_fee` for both events and then called `calculate` with the expression `700*0.90`. The final result was ₹630.

For the comparison question, the agent retrieved both event fees and used the calculator with `500-200`. The difference was ₹300.

For the welcome-message question, the agent did not need to use a tool and directly generated the response.

This demonstrates that the agent can decide when application tools are needed and use their results to produce a final response.

---

## 5. Challenge Task

A new question was given to the agent:

"Can I register for TECHFEST2026 and AIWORKSHOP2026 with a budget of ₹600?"

The agent retrieved the fees using the `get_event_fee` tool.

The combined registration cost was:

₹500 + ₹200 = ₹700

Since ₹700 is greater than the available budget of ₹600, the combined registration exceeds the budget by ₹100.

This demonstrates that the agent can handle a new multi-step question using the available tools rather than relying only on predefined question patterns.

---

## 6. Comparison

| Feature | Plain Chatbot | Rule-Based Workflow | AI Agent |
|---|---|---|---|
| Flexibility | High for natural language | Low for unexpected formats | High |
| Decision-making | Generates responses | Uses predefined conditions | Decides when to use tools |
| Tool usage | No | No | Yes |
| Private-data access | No direct access | Yes | Yes, through tools |
| Multi-step handling | Limited for private data | Predefined steps | Can combine multiple tool calls |
| Automation | Conversational responses | Fixed automated rules | Dynamic tool-based automation |
| Reliability | May not know private data | Reliable for defined rules | Depends on correct tool selection and LLM behavior |

---

## 7. Advantages and Limitations

### Plain Chatbot

Advantages:
- Simple to implement.
- Produces natural-language responses.
- Handles general conversational questions well.

Limitations:
- Cannot automatically access private application data.
- May ask the user for information that is already stored in the application.
- Cannot reliably perform application-specific operations without additional integration.

### Rule-Based Workflow

Advantages:
- Simple and predictable.
- Uses private data directly.
- Produces consistent results for predefined cases.

Limitations:
- Requires explicit rules.
- New or differently phrased questions may not match existing conditions.
- Becomes harder to maintain as the number of rules increases.

### AI Agent

Advantages:
- Can understand natural-language requests.
- Can access private data through tools.
- Can perform multiple tool calls.
- Can handle multi-step tasks.
- Can decide when a tool is required.

Limitations:
- Depends on the LLM correctly selecting and using tools.
- More complex to implement than a simple chatbot or rule-based workflow.
- Tool-use behavior can vary depending on the model.

---

## 8. When Each Approach Is Suitable

A plain chatbot is suitable when the task mainly requires general conversation or text generation and does not require access to private application data.

A rule-based workflow is suitable when the requirements are clearly defined and predictable and consistent rule-based processing is sufficient.

An AI agent is suitable when the task requires natural-language understanding, access to private data or external tools, and multiple steps to complete a request.

---

## 9. Conclusion

The experiment shows the difference between a plain chatbot, a rule-based workflow, and an AI agent.

The plain chatbot relies mainly on the LLM and does not automatically know the private event information. The rule-based workflow can access the private data and provide reliable results for predefined cases, but it depends on explicitly written rules. The AI agent combines an LLM with tools and a loop, allowing it to retrieve private information and perform calculations dynamically.

Therefore, the appropriate approach depends on the requirements of the application: general conversation can use a chatbot, predictable predefined tasks can use a rule-based workflow, and dynamic multi-step tasks requiring tools can use an AI agent.