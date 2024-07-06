import pathlib
import textwrap
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from google.api_core import retry
import json


transcript = YouTubeTranscriptApi.get_transcript('SiBw7os-_zI&t')
genai.configure(api_key='AIzaSyBoC1c2sxmQmgHiIVHirz9Fk388659Arj8')

data_schema = genai.protos.Schema(
    type = genai.protos.Type.OBJECT,
    properties = {
        'topic':  genai.protos.Schema(type=genai.protos.Type.STRING),
        'description':  genai.protos.Schema(type=genai.protos.Type.STRING),
        'start_time': genai.protos.Schema(type=genai.protos.Type.STRING),
    },
    required=['topic', 'description', 'start_time']
)
data = genai.protos.Schema(
    type=genai.protos.Type.ARRAY,
    items=data_schema
)


# Create the FunctionDeclaration
extract_topics_function = genai.protos.FunctionDeclaration(
    name="extract_topics",
    description="Extract topics from transcript using Gemini.",
    parameters=genai.protos.Schema(
        type=genai.protos.Type.OBJECT,
        properties={
            'extracted_data': data
        }
    )
)
if __name__ == '__main__':
    model = genai.GenerativeModel(
        model_name='models/gemini-1.5-pro-latest',
        tools = [extract_topics_function])


    result = model.generate_content(f"""
                                    Extracts topics/concepts explained along with their small descriptions and start_time from the below transcript: 
                                    {transcript}""",
                                    tool_config={'function_calling_config':'ANY'})

    fc = result.candidates[0].content.parts[0].function_call

    print(json.dumps(type(fc).to_dict(fc), indent=4))
    # Save the structured data to a JSON file
    structured_data = type(fc).to_dict(fc)
    structured_data = structured_data['args']['extracted_data']
    output_file = pathlib.Path('structured_data.json')
    with output_file.open('w') as f:
        json.dump(structured_data, f, indent=2)


