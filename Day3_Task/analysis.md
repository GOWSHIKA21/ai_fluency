# From Prompt to Action: LLM with and without a Tool

## 1. Scenario

For this task, I created a simple college fee lookup scenario. A file named `fees.txt` contains the current course fee information:

- CS101 - Programming Fundamentals: Rs. 12000
- AI202 - Artificial Intelligence: Rs. 18000
- DS301 - Data Science: Rs. 15000

The main question used in the experiment was: "What is the fee for CS101?"

The purpose was to compare a plain LLM response with a response where the LLM has access to an external file-reading tool.

## 2. What is a Large Language Model?

A Large Language Model (LLM) is a model trained on a large amount of text that can understand prompts and generate natural-language responses. It can answer many general questions from the knowledge it learned during training.

For example, in this task, a question such as "What is the capital of India?" does not require information from our local file, so the LLM can answer it directly.

However, the LLM does not automatically know the current contents of my local `fees.txt` file. When I asked the plain LLM, "What is the fee for CS101?", it did not have access to the file and responded that it did not have the current fee information.

This shows that an LLM can generate an answer from its own knowledge, but it cannot automatically access new external information unless that information is provided to it.

## 3. What is an Agent?

An agent is an LLM-based system that can decide when it needs to use an external capability to complete a task.

A plain chat response only generates an answer from the information available in the conversation and the model's knowledge. An agent can use tools when the required information or operation is outside what the model can reliably do on its own.

In this scenario, the tool-enabled system can access `fees.txt`. Instead of depending only on the LLM's internal knowledge, it can obtain the actual fee information and then use that result to answer the question.

## 4. What is a Tool and a Tool Call?

A tool is an external function that gives an LLM access to some capability or information that is outside the model itself.

In this project, the tool is `read_fees()`. It opens `fees.txt`, reads its contents, and returns the contents as text.

A tool call is the action of invoking that function. The tool gives the model a way to obtain the information required for the answer.

The tool's description and parameters tell the model what the tool does, what it can be used for, and what information it requires. This information is important because the model needs to understand the tool's purpose before deciding whether it is useful for a particular question.

## 5. Flow of a Tool Call

The tool-enabled process can be explained step by step.

First, the user asks: "What is the fee for CS101?"

Second, the LLM determines that the fee information is not available from its own knowledge and that an external source is required.

Third, the `read_fees()` tool is called.

Fourth, the tool opens `fees.txt` and returns the course fee information.

Fifth, the returned tool result is given to the LLM.

Finally, the LLM uses the tool result and produces the answer: "The fee for CS101 - Programming Fundamentals is Rs. 12,000."

Therefore, the tool provides the actual information and the LLM converts that information into a natural-language answer.

## 6. Why Should a Tool Return Plain Text on Failure?

A tool should return a readable result even when it encounters a problem instead of raising an exception that completely stops the program.

A readable error allows the LLM or the surrounding agent to understand what went wrong and respond appropriately. For example, if `fees.txt` did not exist, the tool could return a message such as "File not found" instead of terminating the entire program.

This makes the tool interaction easier to understand and allows the system to handle failures more gracefully.

## 7. Comparison Table

| Basis for comparison | Plain LLM prompt (no tool) | LLM with one tool |
|---|---|---|
| Source of the answer | The model's own knowledge and the information in the prompt | Model knowledge plus information returned by the tool |
| Can it fetch or compute information outside its own memory? | No access to the local `fees.txt` file | Yes, it can obtain information through `read_fees()` |
| Reliability on factual or numeric questions | Can be insufficient when the required information is external or unavailable | More reliable for information that the tool can retrieve |
| Transparency | The source of the answer is not available from the local file | The tool call and returned result can be observed |
| Speed / cost | Direct response with no tool execution | Requires an additional tool execution before the final answer |

## 8. Observation

For the first question, "What is the fee for CS101?", the plain LLM was unable to provide the current fee because it did not have access to the local file. It responded that it did not have the current fee information.

When the same type of question was answered using the tool-enabled system, `read_fees()` returned the contents of `fees.txt`. The LLM then used the returned information and correctly answered that the CS101 fee was Rs. 12,000.

For a general question such as "What is the capital of India?", the external fee tool is not necessary because the question does not depend on the contents of the local file.

For the third question, "What is the original fee for AI202?", the tool can retrieve the information from `fees.txt`, where AI202 is listed as Rs. 18,000.

These observations show that the usefulness of a tool depends on the question being asked. A tool is useful when the answer requires information that is not available from the model's own knowledge.

## 9. Suitability and Conclusion

A plain LLM prompt is suitable for general questions that can be answered from the model's available knowledge. It is simple and does not require an additional external operation.

However, when a question depends on information stored in an external file, database, website, or another system, providing an appropriate tool can make the response more reliable. In this experiment, the fee information was stored in `fees.txt`, so the file-reading tool allowed the system to obtain the actual information before generating the final answer.

The main difference demonstrated by this project is that a plain LLM only generates a response from the information available to it, while an LLM with a tool can obtain additional information or perform an operation and then use the result in its response.

Therefore, a plain LLM is sufficient for questions within its available knowledge, while a tool becomes necessary when the task depends on external information or an operation that the model cannot directly access.