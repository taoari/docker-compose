import json
import os
from getpass import getpass
from io import StringIO

import openai
import opentelemetry
import pandas as pd
from openai import OpenAI
from openinference.instrumentation.openai import OpenAIInstrumentor
from openinference.semconv.trace import OpenInferenceSpanKindValues, SpanAttributes
from opentelemetry import trace as trace_api
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk import trace as trace_sdk
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

"""## Custom Tracing

Create the tracer provider setup to Phoenix.
"""

resource = Resource(attributes={})
tracer_provider = trace_sdk.TracerProvider(resource=resource)
span_exporter = OTLPSpanExporter(endpoint="http://localhost:6006/v1/traces")
span_processor = SimpleSpanProcessor(span_exporter=span_exporter)
tracer_provider.add_span_processor(span_processor=span_processor)
trace_api.set_tracer_provider(tracer_provider=tracer_provider)

tracer = trace_api.get_tracer(__name__)

# Because we are using Open AI, we will use this along with our custom instrumentation
OpenAIInstrumentor().instrument(skip_dep_check=True)

import os
from openai import OpenAI

# Initialize an OpenAI client
client = OpenAI()

def llm_call(messages, **kwargs):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    return response.choices[0].message.content


# Sequential

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello, can you help me with something?"}
]
with tracer.start_as_current_span("OpenAI Sequential") as span:
    bot_message = llm_call(messages)
    messages.append({"role": "assistant", "content": bot_message})
    print(bot_message)

    messages.append({"role": "user", "content": 'Are you a robot?'})
    bot_message = llm_call(messages)
    messages.append({"role": "assistant", "content": bot_message})
    print(bot_message)

    span.set_attribute("input.value", 'Are you a robot?')
    span.set_attribute("output.value", bot_message)
    span.set_attribute(SpanAttributes.OPENINFERENCE_SPAN_KIND, OpenInferenceSpanKindValues.CHAIN.value)
    span.set_status(trace_api.StatusCode.OK)

# Tree

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello, can you help me with something?"}
]

with tracer.start_as_current_span("OpenAI Tree") as span:
    bot_message = llm_call(messages)
    messages.append({"role": "assistant", "content": bot_message})
    print(bot_message)
    span.set_attribute(SpanAttributes.OPENINFERENCE_SPAN_KIND, OpenInferenceSpanKindValues.CHAIN.value)
    span.set_status(trace_api.StatusCode.OK)

    with tracer.start_as_current_span("OpenAI Inner") as span:
        messages.append({"role": "user", "content": 'Are you a robot?'})
        bot_message = llm_call(messages)
        messages.append({"role": "assistant", "content": bot_message})
        print(bot_message)
        span.set_attribute(SpanAttributes.OPENINFERENCE_SPAN_KIND, OpenInferenceSpanKindValues.CHAIN.value)
        span.set_status(trace_api.StatusCode.OK)


