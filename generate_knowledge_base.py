"""
Run this script once to generate all knowledge base PDFs for TechMart Electronics.
Install dependency first: pip install fpdf2
Then run: python generate_knowledge_base.py
"""

import os
from fpdf import FPDF

os.makedirs("knowledge_base", exist_ok=True)


class PDF(FPDF):
    def __init__(self, doc_title):
        super().__init__()
        self.doc_title = doc_title

    def header(self):
        self.set_fill_color(25, 80, 150)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 14, "TechMart Electronics", border=0, align="C", fill=True)
        self.ln(0)
        self.set_fill_color(52, 120, 210)
        self.set_font("Helvetica", "", 10)
        self.cell(0, 8, self.doc_title, border=0, align="C", fill=True)
        self.ln(10)
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-13)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(130, 130, 130)
        self.cell(0, 8, f"TechMart Electronics  |  Page {self.page_no()}  |  support@techmart.example", align="C")

    def section(self, title):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(25, 80, 150)
        self.ln(4)
        self.cell(0, 8, title)
        self.ln(8)
        self.set_text_color(0, 0, 0)

    def body(self, text):
        self.set_font("Helvetica", "", 11)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 6, text)
        self.ln(3)

    def bullet(self, items):
        self.set_font("Helvetica", "", 11)
        self.set_text_color(40, 40, 40)
        for item in items:
            self.cell(8, 6, "-")
            self.multi_cell(0, 6, item)
        self.ln(2)

    def table_row(self, col1, col2, header=False):
        if header:
            self.set_fill_color(220, 230, 245)
            self.set_font("Helvetica", "B", 11)
        else:
            self.set_fill_color(248, 250, 252)
            self.set_font("Helvetica", "", 11)
        self.cell(80, 7, col1, border=1, fill=True)
        self.cell(110, 7, col2, border=1, fill=True)
        self.ln()


# ─────────────────────────────────────────────
# 1. FAQ.pdf
# ─────────────────────────────────────────────
def create_faq():
    pdf = PDF("Frequently Asked Questions")
    pdf.add_page()

    pdf.section("About TechMart Electronics")
    pdf.body(
        "TechMart Electronics is a leading retailer of laptops, accessories, and software subscriptions. "
        "We serve customers worldwide with fast shipping, dedicated support, and a comprehensive warranty programme."
    )

    pdf.section("Q1. What products does TechMart sell?")
    pdf.body(
        "TechMart offers the ProBook laptop series (ProBook Lite, ProBook X1, ProBook X2), software "
        "subscription plans (Basic, Pro, Premium), and a range of accessories such as mice, keyboards, "
        "docking stations, and laptop bags."
    )

    pdf.section("Q2. How do I contact customer support?")
    pdf.bullet([
        "Email: support@techmart.example",
        "Phone: 1-800-555-0100 (Mon-Fri, 9 am – 6 pm EST)",
        "Live Chat: Available on our website during business hours",
        "Help Center: help.techmart.example (24/7 self-service)",
    ])

    pdf.section("Q3. What are your business hours?")
    pdf.body(
        "Our support team is available Monday to Friday, 9:00 am to 6:00 pm Eastern Standard Time. "
        "Our automated Help Center is available 24 hours a day, 7 days a week."
    )

    pdf.section("Q4. How do I create an account?")
    pdf.body(
        "Visit techmart.example and click 'Sign Up'. Enter your name, email address, and a password "
        "of at least 8 characters. You will receive a verification email within 2 minutes. "
        "Click the link in that email to activate your account."
    )

    pdf.section("Q5. How do I track my order?")
    pdf.body(
        "Once your order ships, you will receive a confirmation email with a tracking number. "
        "You can track your package on the carrier's website or in your TechMart account under "
        "'My Orders'. Tracking updates are available within 24 hours of shipping."
    )

    pdf.section("Q6. What payment methods do you accept?")
    pdf.bullet([
        "Credit/Debit cards: Visa, Mastercard, American Express, Discover",
        "PayPal",
        "Apple Pay and Google Pay",
        "TechMart Gift Cards",
        "Bank transfer (orders above $500 only)",
    ])

    pdf.section("Q7. Can I change or cancel my order?")
    pdf.body(
        "Orders can be modified or cancelled within 1 hour of placement. After that, the order enters "
        "fulfilment and cannot be changed. Contact support@techmart.example immediately if you need "
        "to make changes."
    )

    pdf.section("Q8. How do I reset my password?")
    pdf.body(
        "Click 'Forgot Password' on the login page. Enter your account email address and click Send. "
        "You will receive a password reset link within 5 minutes. The link expires after 30 minutes. "
        "If you do not receive the email, check your spam folder or contact support."
    )

    pdf.section("Q9. Is my data safe with TechMart?")
    pdf.body(
        "Yes. TechMart uses AES-256 encryption for all stored data and TLS 1.3 for data in transit. "
        "We are GDPR and CCPA compliant. We never sell your personal data to third parties. "
        "You can request a copy or deletion of your data at privacy@techmart.example."
    )

    pdf.section("Q10. Do you offer student or business discounts?")
    pdf.body(
        "Yes. Students with a valid university email receive 10% off hardware purchases. "
        "Business customers purchasing 5 or more units qualify for volume pricing. "
        "Contact sales@techmart.example for a custom quote."
    )

    pdf.output("knowledge_base/FAQ.pdf")
    print("Created: knowledge_base/FAQ.pdf")


# ─────────────────────────────────────────────
# 2. RefundPolicy.pdf
# ─────────────────────────────────────────────
def create_refund_policy():
    pdf = PDF("Refund & Return Policy")
    pdf.add_page()

    pdf.section("Overview")
    pdf.body(
        "TechMart Electronics offers a 30-day return window on all eligible products. "
        "Our goal is to ensure every customer is fully satisfied with their purchase. "
        "This policy applies to all orders placed on techmart.example."
    )

    pdf.section("Eligibility for Returns")
    pdf.bullet([
        "Items must be returned within 30 days of the delivery date.",
        "Products must be in original, unused condition with all original packaging.",
        "All accessories, cables, manuals, and warranty cards must be included.",
        "A valid proof of purchase (order number or receipt) is required.",
    ])

    pdf.section("Non-Returnable Items")
    pdf.bullet([
        "Software licences and digital downloads (once activated).",
        "Gift cards.",
        "Items marked 'Final Sale' at the time of purchase.",
        "Products with physical damage caused by the customer.",
        "Items missing serial numbers or with tampered stickers.",
    ])

    pdf.section("How to Initiate a Return")
    pdf.body(
        "Step 1: Log into your TechMart account and go to 'My Orders'.\n"
        "Step 2: Select the order and click 'Request Return'.\n"
        "Step 3: Choose the item(s) and provide a reason for the return.\n"
        "Step 4: Print the prepaid return shipping label sent to your email.\n"
        "Step 5: Pack the item securely and drop it at any authorised courier location."
    )

    pdf.section("Refund Timeline")
    pdf.body(
        "Once we receive and inspect the returned item, we will send you a confirmation email. "
        "Refunds are processed within 2 business days of inspection approval."
    )
    pdf.bullet([
        "Credit/Debit card: 5-7 business days to appear on your statement.",
        "PayPal: 3-5 business days.",
        "TechMart Store Credit: Instant.",
        "Bank transfer: 7-10 business days.",
    ])

    pdf.section("Damaged or Defective Items")
    pdf.body(
        "If you receive a damaged or defective product, contact us within 7 days of delivery "
        "at support@techmart.example with photos of the damage. We will arrange a free replacement "
        "or full refund, including return shipping costs."
    )

    pdf.section("Exchanges")
    pdf.body(
        "We do not offer direct exchanges. To exchange a product, return the original item for a refund "
        "and place a new order for the replacement item. This ensures the fastest processing time."
    )

    pdf.section("Subscription Refunds")
    pdf.body(
        "Software subscription plans may be cancelled at any time. If cancelled within 7 days of "
        "the billing date, a full refund is issued. Cancellations after 7 days take effect at the "
        "end of the current billing cycle with no partial refund."
    )

    pdf.output("knowledge_base/RefundPolicy.pdf")
    print("Created: knowledge_base/RefundPolicy.pdf")


# ─────────────────────────────────────────────
# 3. ShippingPolicy.pdf
# ─────────────────────────────────────────────
def create_shipping_policy():
    pdf = PDF("Shipping Policy")
    pdf.add_page()

    pdf.section("Domestic Shipping (United States)")
    pdf.table_row("Shipping Option", "Estimated Delivery Time", header=True)
    pdf.table_row("Standard Shipping", "3-5 business days")
    pdf.table_row("Express Shipping", "1-2 business days")
    pdf.table_row("Overnight Shipping", "Next business day (order by 2 pm EST)")
    pdf.table_row("Free Standard Shipping", "3-5 business days (orders over $99)")
    pdf.ln(4)

    pdf.section("Shipping Costs")
    pdf.table_row("Order Value", "Shipping Cost", header=True)
    pdf.table_row("Under $99", "$6.99 standard / $14.99 express")
    pdf.table_row("$99 - $499", "Free standard / $9.99 express")
    pdf.table_row("$500 and above", "Free standard and express")
    pdf.ln(4)

    pdf.section("International Shipping")
    pdf.body(
        "TechMart ships to over 50 countries. International delivery times and costs vary by destination."
    )
    pdf.table_row("Region", "Estimated Delivery Time", header=True)
    pdf.table_row("Canada & Mexico", "5-8 business days")
    pdf.table_row("Europe", "7-12 business days")
    pdf.table_row("Asia-Pacific", "10-15 business days")
    pdf.table_row("Rest of World", "12-20 business days")
    pdf.ln(4)

    pdf.section("Order Processing")
    pdf.body(
        "Orders placed before 2:00 pm EST on a business day are processed the same day. "
        "Orders placed after 2:00 pm EST or on weekends and public holidays are processed "
        "the next business day. You will receive a shipping confirmation email with a tracking "
        "number once your order has been dispatched."
    )

    pdf.section("Tracking Your Order")
    pdf.body(
        "All orders include free tracking. Your tracking number will be emailed to you within "
        "24 hours of shipment. You can also view tracking information in your TechMart account "
        "under 'My Orders'. Tracking updates may take up to 24 hours to appear after shipment."
    )

    pdf.section("Lost or Stolen Packages")
    pdf.body(
        "If your tracking shows 'Delivered' but you have not received your package, please: "
        "check with neighbours and building management, wait 24 hours in case of early delivery scans, "
        "then contact us at support@techmart.example. We will open a carrier investigation within "
        "1 business day. If the package is confirmed lost, we will reship or issue a full refund."
    )

    pdf.section("Address Changes")
    pdf.body(
        "Shipping addresses can only be changed before the order is shipped. Contact "
        "support@techmart.example immediately after placing your order if you need to update "
        "your address. Once shipped, address changes are at the carrier's discretion and may "
        "incur additional fees."
    )

    pdf.output("knowledge_base/ShippingPolicy.pdf")
    print("Created: knowledge_base/ShippingPolicy.pdf")


# ─────────────────────────────────────────────
# 4. Warranty.pdf
# ─────────────────────────────────────────────
def create_warranty():
    pdf = PDF("Warranty Information")
    pdf.add_page()

    pdf.section("Standard Limited Warranty")
    pdf.body(
        "All TechMart Electronics hardware products are covered by a 1-year Limited Warranty "
        "from the date of original purchase. This warranty covers defects in materials and "
        "workmanship under normal use conditions."
    )

    pdf.section("What Is Covered")
    pdf.bullet([
        "Manufacturing defects in hardware components.",
        "Faulty display screens (dead pixels exceeding 5 per panel).",
        "Battery defects (capacity falling below 80% within the first year under normal use).",
        "Keyboard, trackpad, and port malfunctions not caused by physical damage.",
        "Internal component failures (RAM, SSD, motherboard) under normal use.",
    ])

    pdf.section("What Is NOT Covered")
    pdf.bullet([
        "Physical damage from drops, spills, or misuse.",
        "Damage from unauthorised modifications or repairs.",
        "Cosmetic damage such as scratches, dents, or broken plastic.",
        "Damage caused by operating outside permitted environmental conditions.",
        "Consumable parts such as batteries after 1 year.",
        "Software issues, viruses, or data loss.",
        "Theft or loss.",
    ])

    pdf.section("Extended Warranty (TechMart Care+)")
    pdf.body(
        "TechMart Care+ extends your warranty coverage to 3 years and adds accidental damage protection."
    )
    pdf.table_row("Plan", "Price", header=True)
    pdf.table_row("TechMart Care+ 2-Year", "$79.99 (one-time)")
    pdf.table_row("TechMart Care+ 3-Year", "$129.99 (one-time)")
    pdf.table_row("TechMart Care+ 3-Year with Accidental Damage", "$179.99 (one-time)")
    pdf.ln(4)

    pdf.section("How to Claim Your Warranty")
    pdf.body(
        "Step 1: Contact support@techmart.example or call 1-800-555-0100.\n"
        "Step 2: Provide your order number, serial number, and a description of the issue.\n"
        "Step 3: Our team will diagnose the issue remotely (usually within 24 hours).\n"
        "Step 4: If the issue cannot be resolved remotely, we will issue a prepaid shipping label.\n"
        "Step 5: Send the device to our repair centre. Repair or replacement takes 5-10 business days.\n"
        "Step 6: Your device will be returned to you with free shipping."
    )

    pdf.section("Warranty Transferability")
    pdf.body(
        "The TechMart standard warranty is transferable to a new owner if the product is sold or gifted "
        "within the first year. The warranty period does not reset upon transfer. TechMart Care+ plans "
        "are non-transferable."
    )

    pdf.section("Contact for Warranty Claims")
    pdf.bullet([
        "Email: warranty@techmart.example",
        "Phone: 1-800-555-0100 (Mon-Fri, 9 am – 6 pm EST)",
        "Please have your order number and serial number ready.",
    ])

    pdf.output("knowledge_base/Warranty.pdf")
    print("Created: knowledge_base/Warranty.pdf")


# ─────────────────────────────────────────────
# 5. Pricing.pdf
# ─────────────────────────────────────────────
def create_pricing():
    pdf = PDF("Product Pricing Guide")
    pdf.add_page()

    pdf.section("Laptop Hardware – ProBook Series")
    pdf.table_row("Model", "Price (USD)", header=True)
    pdf.table_row("ProBook Lite", "$599")
    pdf.table_row("ProBook X1", "$899")
    pdf.table_row("ProBook X2", "$1,199")
    pdf.table_row("ProBook X2 Pro (16 GB RAM upgrade)", "$1,399")
    pdf.ln(4)

    pdf.section("Software Subscription Plans (Monthly)")
    pdf.table_row("Plan", "Monthly Price (USD)", header=True)
    pdf.table_row("Basic", "$9.99 / month")
    pdf.table_row("Pro", "$29.99 / month")
    pdf.table_row("Premium", "$49.99 / month")
    pdf.table_row("Enterprise (per seat)", "$15.00 / month per user")
    pdf.ln(4)

    pdf.section("Software Subscription Plans (Annual – Save 20%)")
    pdf.table_row("Plan", "Annual Price (USD)", header=True)
    pdf.table_row("Basic Annual", "$95.90 / year")
    pdf.table_row("Pro Annual", "$287.90 / year")
    pdf.table_row("Premium Annual", "$479.90 / year")
    pdf.ln(4)

    pdf.section("Accessories")
    pdf.table_row("Accessory", "Price (USD)", header=True)
    pdf.table_row("TechMart Wireless Mouse", "$29.99")
    pdf.table_row("TechMart Mechanical Keyboard", "$79.99")
    pdf.table_row("USB-C Docking Station (7-in-1)", "$59.99")
    pdf.table_row("ProBook Laptop Bag (15\")", "$39.99")
    pdf.table_row("65W USB-C Charger", "$34.99")
    pdf.table_row("Privacy Screen Filter (15\")", "$24.99")
    pdf.ln(4)

    pdf.section("Extended Warranty Pricing")
    pdf.table_row("Plan", "Price (USD)", header=True)
    pdf.table_row("TechMart Care+ 2-Year", "$79.99")
    pdf.table_row("TechMart Care+ 3-Year", "$129.99")
    pdf.table_row("TechMart Care+ 3-Year + Accidental Damage", "$179.99")
    pdf.ln(4)

    pdf.section("Volume & Business Discounts")
    pdf.table_row("Quantity", "Discount", header=True)
    pdf.table_row("5-9 units", "5% off")
    pdf.table_row("10-24 units", "10% off")
    pdf.table_row("25-49 units", "15% off")
    pdf.table_row("50+ units", "Contact sales@techmart.example for custom pricing")
    pdf.ln(4)

    pdf.section("Taxes & Fees")
    pdf.body(
        "All prices listed are exclusive of applicable taxes. Sales tax is calculated at checkout "
        "based on your shipping address. International orders may be subject to import duties and "
        "customs fees, which are the buyer's responsibility."
    )

    pdf.output("knowledge_base/Pricing.pdf")
    print("Created: knowledge_base/Pricing.pdf")


# ─────────────────────────────────────────────
# 6. Products.pdf
# ─────────────────────────────────────────────
def create_products():
    pdf = PDF("Product Catalogue")
    pdf.add_page()

    pdf.section("ProBook Lite – $599")
    pdf.body("Best for: Students and everyday users who need a lightweight, affordable laptop.")
    pdf.table_row("Specification", "Details", header=True)
    pdf.table_row("Processor", "Intel Core i5-1335U (10 cores, up to 4.6 GHz)")
    pdf.table_row("RAM", "8 GB LPDDR5")
    pdf.table_row("Storage", "256 GB NVMe SSD")
    pdf.table_row("Display", "14\" FHD (1920x1080) IPS, 60 Hz")
    pdf.table_row("Battery Life", "Up to 10 hours")
    pdf.table_row("Weight", "1.4 kg (3.1 lbs)")
    pdf.table_row("Operating System", "Windows 11 Home")
    pdf.table_row("Ports", "2x USB-A, 1x USB-C, HDMI, 3.5mm audio")
    pdf.ln(4)

    pdf.section("ProBook X1 – $899")
    pdf.body("Best for: Professionals and power users who need strong performance and all-day battery.")
    pdf.table_row("Specification", "Details", header=True)
    pdf.table_row("Processor", "Intel Core i7-1355U (10 cores, up to 5.0 GHz)")
    pdf.table_row("RAM", "16 GB LPDDR5")
    pdf.table_row("Storage", "512 GB NVMe SSD")
    pdf.table_row("Display", "15.6\" FHD (1920x1080) IPS, 120 Hz, anti-glare")
    pdf.table_row("Battery Life", "Up to 14 hours")
    pdf.table_row("Weight", "1.7 kg (3.7 lbs)")
    pdf.table_row("Operating System", "Windows 11 Pro")
    pdf.table_row("Ports", "2x USB-A, 2x USB-C (Thunderbolt 4), HDMI 2.0, SD card, 3.5mm audio")
    pdf.ln(4)

    pdf.section("ProBook X2 – $1,199")
    pdf.body("Best for: Creators, developers, and power users needing maximum performance.")
    pdf.table_row("Specification", "Details", header=True)
    pdf.table_row("Processor", "Intel Core i9-1355U (10 cores, up to 5.4 GHz)")
    pdf.table_row("RAM", "32 GB LPDDR5 (upgradeable to 64 GB)")
    pdf.table_row("Storage", "1 TB NVMe SSD")
    pdf.table_row("Display", "16\" 2K QHD (2560x1600) IPS, 165 Hz, sRGB 100%")
    pdf.table_row("GPU", "NVIDIA GeForce RTX 3050 (4 GB GDDR6)")
    pdf.table_row("Battery Life", "Up to 12 hours")
    pdf.table_row("Weight", "2.1 kg (4.6 lbs)")
    pdf.table_row("Operating System", "Windows 11 Pro")
    pdf.table_row("Ports", "3x USB-A, 2x Thunderbolt 4, HDMI 2.1, SD card reader, Ethernet, 3.5mm")
    pdf.ln(4)

    pdf.section("Software Subscription Plans")
    pdf.table_row("Feature", "Basic", header=True)
    pdf.table_row("Cloud Storage", "10 GB")
    pdf.table_row("Devices", "1 device")
    pdf.table_row("Support", "Email only")
    pdf.table_row("TechMart Suite Apps", "Basic apps only")
    pdf.ln(2)
    pdf.table_row("Feature", "Pro / Premium", header=True)
    pdf.table_row("Cloud Storage", "100 GB / 1 TB")
    pdf.table_row("Devices", "Up to 3 / unlimited")
    pdf.table_row("Support", "Email + Chat / Priority phone")
    pdf.table_row("TechMart Suite Apps", "All apps + Pro tools / All apps + AI features")
    pdf.ln(4)

    pdf.section("Accessories Overview")
    pdf.bullet([
        "TechMart Wireless Mouse – Ergonomic, 6-button, 2.4 GHz, 12-month battery life.",
        "TechMart Mechanical Keyboard – Compact TKL layout, blue switches, RGB backlight.",
        "USB-C Docking Station (7-in-1) – HDMI, 3x USB-A, USB-C PD 100W, SD, microSD.",
        "ProBook Laptop Bag – Water-resistant, fits up to 15.6\", padded compartment.",
        "65W USB-C Charger – GaN technology, compact, compatible with all ProBook models.",
    ])

    pdf.output("knowledge_base/Products.pdf")
    print("Created: knowledge_base/Products.pdf")


# ─────────────────────────────────────────────
# 7. InstallationGuide.pdf
# ─────────────────────────────────────────────
def create_installation_guide():
    pdf = PDF("Installation Guide")
    pdf.add_page()

    pdf.section("System Requirements")
    pdf.table_row("Requirement", "Minimum / Recommended", header=True)
    pdf.table_row("Operating System", "Windows 10 (64-bit) / Windows 11")
    pdf.table_row("Processor", "Intel Core i3 or AMD Ryzen 3 / i5 or Ryzen 5")
    pdf.table_row("RAM", "4 GB / 8 GB or more")
    pdf.table_row("Storage", "2 GB free space / 5 GB free space")
    pdf.table_row("Internet Connection", "Required for activation and updates")
    pdf.table_row("Browser (Web App)", "Chrome 100+, Firefox 100+, Edge 100+, Safari 15+")
    pdf.ln(4)

    pdf.section("Step 1 – Download the Installer")
    pdf.body(
        "Log into your TechMart account at techmart.example. Go to 'My Products' and click "
        "'Download' next to your software. The installer file (TechMartSetup.exe for Windows, "
        "TechMartSetup.dmg for Mac) will download to your Downloads folder."
    )

    pdf.section("Step 2 – Run the Installer")
    pdf.body(
        "Windows: Double-click TechMartSetup.exe. If prompted by User Account Control (UAC), "
        "click 'Yes' to allow the installation.\n\n"
        "Mac: Open TechMartSetup.dmg, drag the TechMart icon to your Applications folder, "
        "then open it from Applications."
    )

    pdf.section("Step 3 – Accept the Licence Agreement")
    pdf.body(
        "Read the End User Licence Agreement (EULA). Click 'I Agree' to proceed. "
        "If you do not agree, click 'Cancel' to exit the installer."
    )

    pdf.section("Step 4 – Choose Installation Folder")
    pdf.body(
        "The default installation path is C:\\Program Files\\TechMart on Windows. "
        "You may click 'Browse' to choose a different location. We recommend using the default path. "
        "Click 'Install' to begin."
    )

    pdf.section("Step 5 – Activate Your Licence")
    pdf.body(
        "Once installed, launch TechMart and sign in with your account credentials. "
        "Your subscription will activate automatically. If activation fails, check your internet "
        "connection and try again. You may also enter your licence key manually under "
        "Settings > Account > Enter Licence Key."
    )

    pdf.section("Step 6 – Install Updates")
    pdf.body(
        "After installation, the application will check for updates automatically. "
        "We recommend installing all available updates before use to ensure the best performance "
        "and security. Updates can also be triggered manually via Help > Check for Updates."
    )

    pdf.section("Troubleshooting Common Installation Issues")
    pdf.bullet([
        "Error: 'Installation failed – insufficient permissions' → Right-click the installer and select 'Run as Administrator'.",
        "Error: 'VCRUNTIME140.dll is missing' → Download and install the Microsoft Visual C++ Redistributable from microsoft.com.",
        "Error: 'This app cannot run on your PC' → Ensure you downloaded the correct version (32-bit vs 64-bit).",
        "Antivirus blocking installation → Temporarily disable real-time protection during installation, then re-enable it.",
        "Licence activation fails → Ensure your subscription is active at techmart.example/account and that your system clock is correct.",
    ])

    pdf.section("Uninstalling TechMart Software")
    pdf.body(
        "Windows: Go to Settings > Apps > Installed Apps, find TechMart, and click 'Uninstall'.\n"
        "Mac: Open Finder > Applications, right-click TechMart, and select 'Move to Trash'.\n"
        "Your account data and saved files are stored in the cloud and will not be deleted."
    )

    pdf.output("knowledge_base/InstallationGuide.pdf")
    print("Created: knowledge_base/InstallationGuide.pdf")


# ─────────────────────────────────────────────
# 8. UserManual.pdf
# ─────────────────────────────────────────────
def create_user_manual():
    pdf = PDF("User Manual")
    pdf.add_page()

    pdf.section("Getting Started")
    pdf.body(
        "Welcome to TechMart Electronics. This manual covers account setup, the TechMart dashboard, "
        "subscription management, and how to get the most out of your TechMart products and services."
    )

    pdf.section("Creating and Setting Up Your Account")
    pdf.body(
        "1. Visit techmart.example and click 'Sign Up'.\n"
        "2. Enter your full name, email address, and a strong password (minimum 8 characters, "
        "must include a number and a special character).\n"
        "3. Check your email for a verification link and click it within 24 hours.\n"
        "4. Complete your profile by adding your phone number and billing address.\n"
        "5. Enable Two-Factor Authentication (2FA) under Settings > Security for added protection."
    )

    pdf.section("Navigating the Dashboard")
    pdf.bullet([
        "Home – Overview of your active subscriptions, recent orders, and quick actions.",
        "My Orders – Full order history with tracking information and invoice downloads.",
        "My Products – Software downloads, licence keys, and subscription management.",
        "Support – Open a support ticket, live chat, or browse the Help Center.",
        "Account Settings – Update personal details, password, 2FA, and notification preferences.",
        "Billing – View payment history, update payment method, and manage auto-renewal.",
    ])

    pdf.section("Managing Your Subscription")
    pdf.body(
        "To upgrade or downgrade your plan:\n"
        "1. Go to My Products > Manage Subscription.\n"
        "2. Select the new plan and click 'Switch Plan'.\n"
        "3. Upgrades take effect immediately; you are charged a prorated amount for the remainder "
        "of the billing cycle.\n"
        "4. Downgrades take effect at the start of the next billing cycle.\n\n"
        "To cancel your subscription:\n"
        "1. Go to My Products > Manage Subscription > Cancel Plan.\n"
        "2. Select a cancellation reason and confirm.\n"
        "3. Your subscription remains active until the end of the paid period."
    )

    pdf.section("Using TechMart Suite Applications")
    pdf.bullet([
        "TechMart Write – Word processor with real-time collaboration and cloud sync.",
        "TechMart Sheet – Spreadsheet application with built-in charting and formula engine.",
        "TechMart Slides – Presentation tool with 50+ professional templates.",
        "TechMart Vault – Encrypted cloud storage with file versioning (up to 30 versions).",
        "TechMart Meet – Video conferencing for up to 50 participants (Pro) or 200 (Premium).",
        "TechMart AI Assistant – AI-powered writing and data analysis tool (Premium only).",
    ])

    pdf.section("Cloud Storage and File Management")
    pdf.body(
        "All TechMart subscriptions include cloud storage accessible from any device. "
        "Files are automatically synced when you are connected to the internet. "
        "Offline access can be enabled for specific files by right-clicking and selecting "
        "'Make Available Offline'. File deletions are recoverable from the Trash folder for 30 days."
    )

    pdf.section("Security Best Practices")
    pdf.bullet([
        "Enable Two-Factor Authentication (2FA) using an authenticator app such as Google Authenticator.",
        "Never share your password or licence key with anyone.",
        "Use a unique password for your TechMart account.",
        "Log out of shared or public devices after use.",
        "Review active sessions under Settings > Security > Active Sessions and revoke any unfamiliar ones.",
    ])

    pdf.section("Getting Help and Support")
    pdf.body(
        "Help Center: Browse thousands of articles at help.techmart.example.\n"
        "Live Chat: Available from the Support tab in your dashboard (Mon-Fri, 9 am – 6 pm EST).\n"
        "Email Support: support@techmart.example – response within 24 hours.\n"
        "Phone Support: 1-800-555-0100 (Priority support for Pro and Premium subscribers).\n"
        "Community Forum: community.techmart.example – ask questions and share tips."
    )

    pdf.section("Keyboard Shortcuts")
    pdf.table_row("Action", "Windows / Mac Shortcut", header=True)
    pdf.table_row("New Document", "Ctrl+N / Cmd+N")
    pdf.table_row("Save", "Ctrl+S / Cmd+S")
    pdf.table_row("Search", "Ctrl+F / Cmd+F")
    pdf.table_row("Settings", "Ctrl+, / Cmd+,")
    pdf.table_row("Upload File", "Ctrl+U / Cmd+U")
    pdf.table_row("Logout", "Ctrl+Shift+Q / Cmd+Shift+Q")
    pdf.ln(4)

    pdf.output("knowledge_base/UserManual.pdf")
    print("Created: knowledge_base/UserManual.pdf")


# ─────────────────────────────────────────────
# Run all generators
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("Generating TechMart Electronics knowledge base...\n")
    create_faq()
    create_refund_policy()
    create_shipping_policy()
    create_warranty()
    create_pricing()
    create_products()
    create_installation_guide()
    create_user_manual()
    print("\nAll 8 PDFs created in the knowledge_base/ folder.")
