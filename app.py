#copywriting-generator

from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
import os
import openai
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Alignment
import pandas as pd
import bcrypt

app = Flask(__name__)

# Define the creative_text variable here and initialize it with an empty string
creative_text = ""

# Configure your OpenAI API key
api_key = os.environ.get('copygpt')
openai.api_key = api_key

#uwierzytelnienie
authenticated = False

password = b'$2a$10$Tz2xdbpb14ChVIkEvCRV7.AbJVIOMnGrctKBo6VnvpwEu4391.wsW'

@app.route('/login', methods=['GET', 'POST'])
def login():
    global authenticated

    if request.method == 'POST':
        password_attempt = request.form.get('password')

        if bcrypt.checkpw(password_attempt.encode('utf-8'), password):
            authenticated = True
            return redirect(url_for('index'))
        else:
            return "Złe hasło. Spróbuje ponownie."

    return render_template('login.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    global creative_text  # Declare creative_text as a global variable

    if not authenticated:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Read input data from the selected Excel (xlsx) file
        input_file = request.files['file']
        input_file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(input_file.filename))
        input_file.save(input_file_path)

        df = pd.read_excel(input_file_path)
        creative_text = ""  # Reset creative_text to an empty string for each POST request
        for column in df.columns:
            creative_text += " ".join(df[column].astype(str)) + " "

        # Get the selected marketplace from the form
        selected_marketplace = request.form['marketplace']

        # Define rulesets based on the selected marketplace
        if selected_marketplace == 'kaufland':
            ruleset = Kaufland_ruleset
        # elif selected_marketplace == 'cdiscount':
        #     ruleset = Cdiscount_ruleset
        # elif selected_marketplace == 'ebay':
        #     ruleset = ebay_ruleset
        else:
            # Handle other marketplaces or invalid selections here
            return "Invalid marketplace selection"

        openai.api_key = api_key

        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": ruleset},
                {"role": "user", "content": creative_text},
            ],
            max_tokens=6000,
            temperature=1.0
        )

        # Extract the AI-generated response
        response = completion.choices[0].message["content"]

        # Add the response to your DataFrame
        df["Generated Response"] = response

        # Save the modified DataFrame back to a new Excel file
        output_file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{selected_marketplace}.xlsx")
        df.to_excel(output_file_path, index=False)

        return redirect(url_for('download_file', filename=f"{selected_marketplace}.xlsx"))

    return render_template('index.html')

# Configuration for file upload
app.config['UPLOAD_FOLDER'] = os.path.abspath('uploads')  # Use an absolute path

@app.route('/download/<filename>')
def download_file(filename):
    # Get the absolute path of the modified file
    file_path = os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return send_file(file_path, as_attachment=True)

Kaufland_ruleset = (
    f"Based on the following rules, make changes to {creative_text}"
    "Title:"
    "- Formal guidelines:"
    "- Correct language and grammar."
    "- No symbols, emoticons, or unusual characters."
    "- Use of numerical notation (e.g., 15 instead of fifteen)."
    "- Consistent formatting (e.g., all uppercase or camelCase), except for brand names."
    "- Short and clear product titles."
    "- No repeated content."
    "- Contains key product information."
    "- No price or product availability-related advertising."
    "- No seller information."
    "- Recommended title length: 50 to 80 characters."

    "Description:"
    "- Formal guidelines:"
    "- Text in HTML format."
    "- Correct language and grammar (no automatic translations)."
    "- No JavaScript code."
    "- Well-formatted descriptions (plain text or HTML) with paragraphs and bold headers."
    "- No special fonts, list symbols, or unusual characters."
    "- Clear and consistent information to help the customer understand the product."
    "- No obscene, illegal, or promotional content."
    "- Consistent information without incorrect details."
    "- No health claims or keyword spam."
    "- No product condition, shipping, or contact information."
    "- No prices, discounts, or warranty information."
    "- No explanations regarding product testing."
    "- Recommended description length: 150 to 5000 characters."

    "Short Description:"
    "- Formal guidelines:"
    "- Keywords are separated by commas."
    "- No code, HTML, emoticons, or unusual characters."
    "- Error-free language, plain text, and numbers."
    "- Only relevant keywords, no keyword spam."
    "- Maximum of 10 keywords recommended."
)


Cdiscount_ruleset = (
    f"Generate a product title, short basket label, long wording, product description, and encoded marketing description for the following product based on the provided guidelines:\n"
    
    "1. Product Title (Labels):\n"
    "- The product title must be written in French and contain the main product information for the purchaser. As a minimum, the title must contain: [Brand] – [Product type] – [Description keywords] – [Model] (for technical products) – [Gender] (if applicable).\n"
    "- Short Basket Label (Limited to 30 characters):\n"
    "   - It must contain, as far as possible (and the limit of the number of characters allowed) the exact references of the product, and imperatively the mark. Example: KODAK Easyshare M530 Orange, salon MANO 6P résine tressée, BAMBISOL Combiné Trio Illico Bora.\n"
    "   - Texts in French/No rough translations from a foreign language.\n"
    "   - Correct spelling.\n"
    "   - No abbreviations or special characters (slash, anti-slash, etc.), symbols.\n"
    "   - No URL or HTML in the wordings.\n"
    "   - No offer data.\n"
    "- Long Wording (Limited to 132 characters):\n"
    "   - Texts in French/No rough translations from a foreign language.\n"
    "   - Correct spelling.\n"
    "   - Wording must state the product type.\n"
    "   - Minimum criteria to enter: [Brand] – [Product type] – [Description keywords] – [Model] (for technical products) – [Gender] (if applicable).\n"
    "   - No abbreviations or special characters (slash, anti-slash, etc.), symbols.\n"
    "   - No URL or HTML in the wordings.\n"
    "   - Do not put in too many keywords or parasite words (i.e.: Evening, wedding, christening, bar mitzvah, communion dress).\n"
    "   - No offer data.\n"

    "2. Product Description (Limited to 420 characters):\n"
    "- The product description. Put yourself in the purchaser’s position and give them the information they need to make a purchase. Warning, only product-specific information which does not change from one vendor to another.\n"
    "- Texts in French/No rough translations from a foreign language.\n"
    "- Correct spelling.\n"
    "- Offer data (prices, delivery, warranty, etc.) are not allowed on the sheets; they must be provided in your offer file.\n"
    "- No HTML code.\n"

    "3. Encoded Marketing Description (Limited to 5000 characters):\n"
    "- It allows you to add images, videos, and HTML.\n"
    "- Texts in French/No rough translations from a foreign language.\n"
    "- Construct your sentences with subjects, verbs, and complements, avoid telegraphic style.\n"
    "- Correct spelling.\n"
    "- Add HTML code for a quality description.\n"
    "- Offer data (prices, delivery, warranty, etc.) are not allowed on the sheets; they must be provided in your offer file.\n"
    "- Never enter marks that do not correspond to the product sold (e.g., as a Nespresso for a non-branded or non-branded coffee maker).\n"

)

ebay_ruleset = (

    "Title Prompt:\n"
    "\"Create a compelling eBay listing title for a [product type]\"\n\n"
    "Guidelines:\n"
    "1. Ensure the title is clear and concise, with correct spelling, and does not exceed 80 characters.\n"
    "2. Avoid using all capital letters and focus on specific details such as brand, model, size, and color.\n"
    "3. Include up to three keywords or phrases in the title, placing the most important ones at the beginning.\n"
    "4. Highlight that titles with more than 60 characters have a 1.5 times greater chance of selling.\n"
    "5. Follow the format: \"NEW\" [brand] [product name] [model No] [Variants - size, color] [additional keyword]\n"
    "6. Avoid using entire words in capital letters or special characters.\n\n"

    "Description Prompt:\n"
    "\"Compose a comprehensive eBay item description for a [product type]\"\n\n"
    "Guidelines:\n"
    "1. Ensure the description is clear and detailed, providing essential product information.\n"
    "2. Include the item's key selling points and list what's included in the sale (e.g., cables for electronics).\n"
    "3. Use full sentences with correct spelling and punctuation throughout.\n"
    "4. Avoid conflicting product information and unrelated content (e.g., political views or personal information).\n"
    "5. Do not include Top Rated Seller or similar icons or expressions.\n"
    "6. Avoid comments that encourage buyers to rate you.\n"
    "7. Do not use any type of active content like videos, animations, or widgets.\n"
    "8. Keep the description concise and within the eBay word limit (up to 4,000 characters, but prioritize the first 250 characters).\n"
    "9. Mention the use of eBay description tools like Crazylister, Sellbrite, 3D Sellers, or Optiseller for efficiency.\n"
    "10. Consider using HTML for proper alignment, bullets, font changes, etc., if you have coding knowledge.\n\n"

)

if __name__ == "__main__":
    app.run(debug=True)
