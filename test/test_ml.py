# Use a pipeline as a high-level helper
import warnings
from transformers import pipeline
warnings.filterwarnings('ignore')

pipe = pipeline("text2text-generation", model="google/flan-t5-base")


while (var := input(" >>> ") ) != "exit":
    print("question: ", var)
    answer = pipe(var)[0]['generated_text']
    print("answer: ", answer)

