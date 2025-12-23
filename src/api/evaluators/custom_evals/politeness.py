import json
import os
import prompty
# to use the azure invoker make 
# sure to install prompty like this:
# pip install prompty[azure]
import prompty.azure
from prompty.tracer import trace, Tracer, console_tracer, PromptyTracer
from dotenv import load_dotenv
load_dotenv()


# add json tracer for structured logging to .runs/ directory
# this only has to be done once at application startup
json_tracer = PromptyTracer()
Tracer.add("PromptyTracer", json_tracer.tracer)

@trace
def politeness_evaluation(    
      question: any,
      context: any,
      answer: any
) -> str:

  # execute the prompty file
  model_config = {
        "azure_endpoint": os.environ["AZURE_OPENAI_ENDPOINT"],
        "api_version": os.environ["AZURE_OPENAI_API_VERSION"],
  }
  result = prompty.execute(
    "politeness.prompty", 
    inputs={
      "question": question,
      "context": context,
      "answer": answer
    },
    configuration=model_config
  )

  return result

if __name__ == "__main__":
   json_input = '''{
  "question": "How do I reset my password?",
  "context": "Password reset instructions are available in the user manual. Users should click the forgot password link on the login page.",
  "answer": "Just click forgot password. It's obvious."
}'''
   args = json.loads(json_input)

   result = politeness_evaluation(**args)
   print(result)
