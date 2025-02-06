from typing import Dict, Any
from documents import DocumentGenerator
from datetime import datetime

class ProcessManager:
    def __init__(self):
        """Initialize the process manager."""
        self.doc_generator = DocumentGenerator()
        
        # Sample inventory data (in real app, this would come from a database)
        self.inventory = {
            "DTB-2024-BLK": {
                "quantity": 45,
                "location": "Warehouse A, Aisle 12, Rack 3",
                "price": 1500.00
            },
            "PTB-2024-RED": {
                "quantity": 30,
                "location": "Warehouse B, Aisle 10, Rack 5",
                "price": 2500.00
            }
        }
    
    def show_process_chart(self, current_step: str):
        """Display the current position in the process flow."""
        print("\n📊 Current Position in Sales Process:")
        print("=" * 50)
        steps = [
            ("Sales Inquiry", "📝"),
            ("Inventory Check", "🔍"),
            ("Picking", "📦"),
            ("Shipping", "🚚"),
            ("Billing", "💰")
        ]
        
        for step, icon in steps:
            if step == current_step:
                print(f"➡️ {icon} {step} <- You are here")
            else:
                print(f"   {icon} {step}")
        print("=" * 50)
    
    def parse_inquiry(self, inquiry_text: str) -> Dict[str, Any]:
        """Parse the inquiry text into structured data."""
        lines = [line.strip() for line in inquiry_text.split('\n') if line.strip()]
        
        # Extract customer
        customer = lines[0].replace('Customer:', '').strip()
        
        # Generate document number
        date = datetime.now()
        doc_number = f"INQ-{date.strftime('%Y%m%d')}-{customer[:3].upper()}"
        
        # Extract products
        products = []
        for line in lines:
            if line.startswith('-'):
                parts = line.replace('-', '').strip().split()
                quantity = int(parts[0])
                name = ' '.join(parts[1:-2])
                color = parts[-1]
                
                # Generate product ID
                if 'Deluxe' in name:
                    product_id = 'DTB-2024-BLK'
                else:
                    product_id = 'PTB-2024-RED'
                
                products.append({
                    'id': product_id,
                    'name': f"{name} in {color}",
                    'quantity': quantity,
                    'price': self.inventory[product_id]['price']
                })
        
        # Extract delivery and special requirements
        delivery = next((line.replace('Delivery:', '').strip() 
                        for line in lines if line.startswith('Delivery:')), '')
        special_reqs = next((line.replace('Special requirements:', '').strip() 
                           for line in lines if line.startswith('Special')), '')
        
        return {
            "doc_number": doc_number,
            "customer": customer,
            "products": products,
            "delivery": delivery,
            "special_requirements": special_reqs
        }
    
    def process_sales_inquiry(self, inquiry_text: str) -> Dict[str, Any]:
        """Process a sales inquiry through the entire workflow."""
        try:
            print("\n🏢 B2B Sales Process Simulation")
            print("=" * 50)
            
            # Step 1: Process Initial Inquiry
            self.show_process_chart("Sales Inquiry")
            print("\n📝 Processing Sales Inquiry")
            print("-" * 50)
            
            inquiry_data = self.parse_inquiry(inquiry_text)
            inquiry_doc = self.doc_generator.generate_inquiry_document(inquiry_data)
            print(inquiry_doc)
            input("\nPress Enter to continue to inventory check...")
            
            # Step 2: Inventory Check
            self.show_process_chart("Inventory Check")
            print("\n🔍 Checking Inventory")
            print("-" * 50)
            
            inventory_doc = self.doc_generator.generate_inventory_document(
                inquiry_data, self.inventory
            )
            print(inventory_doc)
            
            # Decision Point 1: FG Stock Status
            print("\n❓ Decision Point - Finished Goods (FG) Stock")
            print("1. Sufficient FG stock available")
            print("2. Insufficient FG stock - Check Raw Materials")
            fg_choice = input("Select scenario (1-2): ")
            
            if fg_choice == "2":
                print("\n❓ Decision Point - Raw Materials (RM) Stock")
                print("1. Sufficient RM stock - Can manufacture")
                print("2. Insufficient RM stock - Need to order")
                rm_choice = input("Select scenario (1-2): ")
                
                if rm_choice == "2":
                    print("\n⚠️ Process halted: Insufficient stock and materials")
                    print("\nNext steps would be:")
                    print("1. Order required raw materials")
                    print("2. Update customer about delay")
                    print("3. Reschedule production when materials arrive")
                    print("\n📋 Process Summary:")
                    print("1. Sales Inquiry: Customer order received")
                    print("2. Inventory Check: Insufficient stock identified")
                    print("3. Status: Order processing halted - awaiting materials")
                    return {
                        "status": "halted",
                        "reason": "insufficient_stock",
                        "inquiry_data": inquiry_data
                    }
            
            # Step 3: Picking Process
            self.show_process_chart("Picking")
            print("\n📦 Creating Picking Documents")
            print("-" * 50)
            
            picking_doc = self.doc_generator.generate_picking_document(
                inquiry_data, self.inventory
            )
            print(picking_doc)
            input("\nPress Enter to continue to shipping...")
            
            # Step 4: Shipping Process
            self.show_process_chart("Shipping")
            print("\n🚚 Processing Shipment")
            print("-" * 50)
            
            shipping_doc = self.doc_generator.generate_shipping_documents(
                inquiry_data, {"picking_complete": True}
            )
            print(shipping_doc)
            input("\nPress Enter to continue to billing...")
            
            # Step 5: Billing Process
            self.show_process_chart("Billing")
            print("\n💰 Generating Billing Documents")
            print("-" * 50)
            
            billing_doc = self.doc_generator.generate_billing_documents(
                inquiry_data, {"shipping_complete": True}
            )
            print(billing_doc)
            
            print("\n✅ Process completed successfully!")
            print("\nProcess Summary:")
            print("1. Sales Inquiry: Customer order received and processed")
            print("2. Inventory: Stock availability confirmed")
            print("3. Picking: Items picked from warehouse")
            print("4. Shipping: Goods prepared for shipment")
            print("5. Billing: Invoice and delivery note generated")
            
            return {
                "status": "completed",
                "inquiry_data": inquiry_data
            }
            
        except Exception as e:
            print(f"\n❌ Error: Process halted due to an error")
            print(f"Error details: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            } 