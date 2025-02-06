import streamlit as st
from process_manager import ProcessManager
from datetime import datetime

def initialize_session_state():
    if 'step' not in st.session_state:
        st.session_state.step = 0
        st.session_state.manager = ProcessManager()
        st.session_state.inquiry_processed = False
        st.session_state.fg_choice = None
        st.session_state.rm_choice = None
        st.session_state.process_complete = False

def main():
    st.set_page_config(
        page_title="B2B Sales Process Learning Simulator",
        page_icon="🎓",
        layout="wide"
    )

    initialize_session_state()

    st.title("🎓 B2B Sales Process Learning Simulator")
    st.markdown("*A learning tool for understanding the B2B sales process*")
    st.markdown("---")

    # Sidebar showing current progress
    with st.sidebar:
        st.header("Process Overview")
        steps = [
            ("Introduction", "📚"),
            ("Sales Inquiry", "📝"),
            ("Inventory Check", "🔍"),
            ("Picking", "📦"),
            ("Shipping", "🚚"),
            ("Billing", "💰")
        ]
        
        for i, (step, icon) in enumerate(steps):
            if i == st.session_state.step:
                st.markdown(f"**➡️ {icon} {step}**")
            elif i < st.session_state.step:
                st.markdown(f"✅ {icon} {step}")
            else:
                st.markdown(f"{icon} {step}")

    # Main content area - Step by step process
    if st.session_state.step == 0:
        st.header("Welcome to the B2B Sales Process Simulator")
        st.markdown("""
        This simulator will guide you through a typical B2B sales process in a bicycle manufacturing company.
        You will:
        - Observe how a sales inquiry is processed
        - Make decisions about inventory management
        - Learn about the complete order fulfillment cycle
        
        Click 'Start' when you're ready to begin!
        """)
        
        if st.button("Start"):
            st.session_state.step += 1
            st.rerun()

    elif st.session_state.step == 1:
        st.header("📝 Step 1: Sales Inquiry Processing")
        
        if not st.session_state.inquiry_processed:
            st.markdown("""
            We've received the following sales inquiry from a customer:
            """)
            
            inquiry = """
            Customer: BikeWorld GmbH
            Products requested:
            - 30 Deluxe Touring Bikes in Black
            - 20 Professional Touring Bikes in Red
            Delivery: Needed within 4 weeks
            Special requirements: All bikes must include standard warranty
            """
            
            st.code(inquiry, language="text")
            
            if st.button("Process Inquiry"):
                st.session_state.inquiry_processed = True
                st.rerun()
                
        if st.session_state.inquiry_processed:
            st.success("✅ Sales inquiry has been processed!")
            st.markdown("The system has generated an inquiry document with a unique reference number.")
            
            if st.button("Proceed to Inventory Check"):
                st.session_state.step += 1
                st.rerun()

    elif st.session_state.step == 2:
        st.header("🔍 Step 2: Inventory Check")
        
        if st.session_state.fg_choice is None:
            st.markdown("""
            The system now checks the current inventory levels for the requested products.
            
            ### Decision Point: Finished Goods (FG) Stock
            As the inventory manager, you need to make a decision based on the current stock levels.
            """)
            
            st.info("What is the current stock situation?")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("1. Sufficient FG stock available"):
                    st.session_state.fg_choice = "sufficient"
                    st.rerun()
            with col2:
                if st.button("2. Insufficient FG stock"):
                    st.session_state.fg_choice = "insufficient"
                    st.rerun()
                    
        elif st.session_state.fg_choice == "sufficient":
            st.success("✅ Sufficient stock is available to fulfill the order!")
            if st.button("Proceed to Picking"):
                st.session_state.step += 1
                st.rerun()
                
        elif st.session_state.fg_choice == "insufficient":
            if st.session_state.rm_choice is None:
                st.warning("⚠️ Insufficient finished goods stock detected!")
                st.markdown("""
                ### Decision Point: Raw Materials (RM) Stock
                We need to check if we can manufacture more bikes.
                """)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("1. Sufficient RM stock - Can manufacture"):
                        st.session_state.rm_choice = "sufficient"
                        st.rerun()
                with col2:
                    if st.button("2. Insufficient RM stock - Need to order"):
                        st.session_state.rm_choice = "insufficient"
                        st.rerun()
                        
            elif st.session_state.rm_choice == "sufficient":
                st.success("✅ We can manufacture the required bikes!")
                if st.button("Proceed to Picking"):
                    st.session_state.step += 1
                    st.rerun()
                    
            elif st.session_state.rm_choice == "insufficient":
                st.error("❌ Process halted: Insufficient stock and materials")
                st.markdown("""
                ### Next Steps Would Be:
                1. Order required raw materials
                2. Update customer about delay
                3. Reschedule production when materials arrive
                
                In a real scenario, this would trigger a separate procurement process.
                """)
                
                if st.button("Restart Simulation"):
                    st.session_state.clear()
                    st.rerun()

    elif st.session_state.step == 3:
        st.header("📦 Step 3: Picking Process")
        st.markdown("""
        The system has generated picking documents for the warehouse team.
        
        The following items will be picked:
        - 30 Deluxe Touring Bikes (Black) from Warehouse A, Aisle 12, Rack 3
        - 20 Professional Touring Bikes (Red) from Warehouse B, Aisle 10, Rack 5
        """)
        
        if st.button("Proceed to Shipping"):
            st.session_state.step += 1
            st.rerun()

    elif st.session_state.step == 4:
        st.header("🚚 Step 4: Shipping Process")
        st.markdown("""
        The picked items are now being prepared for shipment.
        
        The system has generated:
        - Packing list
        - Shipping labels
        - Delivery note
        """)
        
        if st.button("Proceed to Billing"):
            st.session_state.step += 1
            st.rerun()

    elif st.session_state.step == 5:
        st.header("💰 Step 5: Billing Process")
        st.markdown("""
        All documents have been generated and the process is complete!
        
        Generated documents:
        - Invoice
        - Delivery note
        - Warranty certificates
        
        ### Process Summary:
        1. Sales Inquiry: Customer order received and processed
        2. Inventory: Stock availability confirmed
        3. Picking: Items picked from warehouse
        4. Shipping: Goods prepared for shipment
        5. Billing: Invoice and delivery note generated
        """)
        
        if st.button("Restart Simulation"):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    main() 