from process_manager import ProcessManager

def main():
    # Initialize the process manager
    manager = ProcessManager()
    
    # Example inquiry
    inquiry = """
    Customer: BikeWorld GmbH
    Products requested:
    - 30 Deluxe Touring Bikes in Black
    - 20 Professional Touring Bikes in Red
    Delivery: Needed within 4 weeks
    Special requirements: All bikes must include standard warranty
    """
    
    # Process the sales inquiry
    try:
        results = manager.process_sales_inquiry(inquiry)
        
        if results["status"] == "completed":
            print("\n✅ Process completed successfully!")
            print("All documents have been generated and the order is ready for processing.")
        elif results["status"] == "halted":
            print("\n⏸️ Process halted")
            print("The order requires attention before it can be processed further.")
        else:
            print("\n❌ Process encountered an error")
            print(f"Error details: {results.get('error', 'Unknown error')}")
        
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    main() 