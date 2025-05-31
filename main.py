from agent.agent import get_patient_agent

def main():
    print("Dermatology Clinic Assistant - Type 'exit' to quit")
    print("-----------------------------------------------")
    
    # Initialize the agent
    agent = get_patient_agent()
    
    # Interactive loop
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
            
        if user_input:
            try:
                # Get response from the agent
                response = agent(user_input)
                print(f"\nAssistant: {response}")
            except Exception as e:
                print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()
