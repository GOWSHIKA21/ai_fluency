# Reasoning and Acting: Direct Prompting, Chain-of-Thought, and ReAct

## 1. Scenario

The scenario selected for this task is a College Event Budget.

The event has a total budget of Rs. 50,000. The venue costs Rs. 12,000, food costs Rs. 8,000, and the rental price of a projector is obtained using an external tool. The scenario also contains reasoning-based questions such as calculating the remaining budget and determining the number of tables required for students.

The purpose of this experiment is to compare Direct Prompting, Chain-of-Thought (CoT), and ReAct approaches for solving different types of questions.

---

## 2. Direct Prompting

Direct prompting asks the language model to provide only the final answer without explicitly requesting a reasoning process.

In this project, the direct prompt was used for three questions related to the college event. The first question asks for the projector rental price, the second asks for the remaining event budget, and the third asks how many tables are required for 120 students when each table seats 6 students.

Direct prompting is simple and fast because the model is asked to provide only the answer. It is suitable for simple questions where the required information is already available in the prompt. However, it provides less transparency because the reasoning or calculation steps are not explicitly shown.

---

## 3. Chain-of-Thought Prompting

Chain-of-Thought prompting asks the model to solve a problem step by step and show the calculation before giving the final answer.

In this experiment, the CoT prompt instructed the model to number the steps, show the calculation, and provide a final answer. This makes the solution easier to inspect because the intermediate reasoning is visible.

For example, the table question can be solved using:

120 students / 6 students per table = 20 tables.

CoT is useful when a question involves multiple calculations or requires a sequence of reasoning steps. The main disadvantage is that the response is longer than direct prompting and therefore can require more output tokens.

---

## 4. ReAct

ReAct combines reasoning with actions performed through external tools.

In this project, two tools were implemented:

1. `get_equipment_price()` - retrieves the rental price of event equipment.
2. `calculator()` - evaluates mathematical expressions.

The ReAct agent first receives the event question and decides whether a tool is required. For the projector price, it can call the equipment-price tool instead of inventing the value. After receiving the tool observation, it can use the information to continue solving the budget problem.

The ReAct approach is useful when a question requires external information or a tool. It makes tool usage visible through the Action and Observation steps. This makes the process more transparent than direct prompting.

---

## 5. Comparison of the Three Approaches

| Criterion | Direct Prompting | Chain-of-Thought | ReAct |
|---|---|---|---|
| Reasoning depth | Low | Higher | Higher with actions |
| Tool usage | No | No | Yes |
| Transparency | Low | High | High |
| Response length | Short | Longer | Depends on tool calls |
| Speed | Usually fast | Usually slower than direct | Can be slower because of tool calls |
| Best suited for | Simple questions | Multi-step reasoning | Questions requiring tools or external information |
| Reliability | Depends on the information given | Useful for calculation-based reasoning | Useful when accurate external/tool information is required |

Direct prompting is appropriate when the answer can be produced directly from the information in the prompt. Chain-of-Thought is useful when a problem requires multiple reasoning steps. ReAct is more suitable when the problem requires both reasoning and interaction with external tools.

---

## 6. Self-Consistency Observation

Self-consistency was tested by running the same reasoning question multiple times with temperature set to 0.8 and then comparing the responses with runs using temperature 0.

The selected question was:

"The event has 120 students. Each table can seat 6 students. How many tables are needed?"

The calculation is:

120 / 6 = 20

Therefore, the correct answer is 20 tables.

The experiment showed that higher temperature can introduce variation in the wording and reasoning style of the generated responses. The final numerical answer remained consistent for this simple problem. Temperature 0 produced more deterministic responses.

This shows that self-consistency can be useful when several reasoning paths are generated and the final answers can be compared to identify a consistent result.

---

## 7. Suitability of Each Approach

Direct prompting is suitable for simple questions where the required information is already known and only a short answer is required.

Chain-of-Thought is suitable for mathematical and logical questions that require multiple steps. Showing intermediate calculations makes the answer easier to inspect and understand.

ReAct is suitable when a problem requires information from an external source, database, API, calculator, or another tool. Instead of relying only on information generated by the model, the agent can take an action, observe the tool result, and continue reasoning.

For the college event scenario, ReAct is particularly useful for obtaining the projector rental price because that information is provided through the equipment-price tool.

---

## 8. Conclusion

This experiment demonstrated three different ways of solving problems with a language model.

Direct prompting provides concise answers and is useful for simple tasks. Chain-of-Thought provides a more detailed reasoning process and is useful for multi-step problems. ReAct extends reasoning by allowing the model to interact with tools and use their observations while solving a problem.

The experiment also demonstrated self-consistency by generating multiple responses to the same reasoning problem. Different temperatures can affect the variation of generated responses.

Overall, the appropriate approach depends on the problem. Simple questions can use direct prompting, calculation-heavy reasoning can use Chain-of-Thought, and problems requiring external information or actions can use ReAct.