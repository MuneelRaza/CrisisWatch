from langchain_core.messages import HumanMessage, AIMessage, ToolMessage



def pretty_print_messages(messages):
    message_output = ""

    for idx, message in enumerate(messages):
        if isinstance(message, HumanMessage):
            # Format HumanMessage
            message_output += f"\n===== 👤 Human Message =====\n"
            content = message.content
            message_output += f"Content: {content}\n"

        elif isinstance(message, AIMessage):
            # Format AIMessage
            message_output += f"\n===== 🤖 AI Message =====\n"
            content = message.content
            message_output += f"Content: {content if content else '[No direct response, tool used]'}\n"

            # Check for tool calls in AIMessage
            if 'tool_calls' in message.additional_kwargs:
                message_output += "Tool Calls:\n"
                tool_calls = message.additional_kwargs["tool_calls"]

                for tool_call in tool_calls:
                    message_output += f"      🔧 Tool: {tool_call['function']['name']}\n"
                    message_output += f"         Arguments: {tool_call['function']['arguments']}\n"                    
                    message_output += f"         ID: {tool_call['id']}\n"


        elif isinstance(message, ToolMessage):
            # Format ToolMessage
            message_output += f"\n===== 🔧 Tool Message =====\n"
            content = message.content
            name = message.name
            tool_call_id = message.tool_call_id
            message_output += "🔧 Tool Message:\n"
            message_output += f"Tool: {name}\n"
            message_output += f"Call_id: {tool_call_id}\n"
            message_output += f"Content: {content}\n"

        else:
            message_output += "\n\n UNKNOWN \n"+str(message)


    message_output += "\n==================================\n"
    return message_output