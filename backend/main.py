def research(question):
    print("Researching:",question)

    return{
        "question": question,
        "status": "Research completed"
    }
question = "What is Artificial Intelligence?"
result = research(question)
print(result)