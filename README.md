# Copywriting Generator

This is a web application for generating product copywriting using OpenAI's GPT-4. It allows you to create compelling and informative product descriptions and titles for various marketplaces. Here's an overview of the key components and functionalities:

## Features

1. **Login Authentication**: Before accessing the copywriting generation functionality, users are required to log in. Authentication is achieved by entering a password, which is securely hashed.

2. **Input Data**: Users can upload an Excel (xlsx) file containing product information. The application processes this data to generate creative copywriting.

3. **Marketplace Selection**: Users can specify the target marketplace for which they want to generate copywriting. Currently, the application supports Kaufland,CDiscount and Ebay but you can extend it to other marketplaces.

4. **Copywriting Generation**: The application utilizes OpenAI's GPT-4 to generate product copywriting based on predefined rulesets specific to the selected marketplace. It ensures that generated content adheres to the marketplace's guidelines and formatting requirements.

5. **Output Excel File**: The generated copywriting is added to the input Excel file, creating a new file with the copywriting included. Users can download this modified Excel file.

## Installation and Usage

To use this application, follow these steps:

1. Clone this repository to your local machine.
2. Install the required dependencies by running `pip install flask openai pandas bcrypt openpyxl`.
3. Set your OpenAI API key as an environment variable named `YOUR_API_KEY`.
4. Hash your desired password and replace `YOUR_HASHED_PASSWORD` with the hashed password in the code.
5. Run the application using `python your_script.py`.
6. Access the application in your web browser at `http://localhost:5000`.

## Rulesets

The application includes rulesets for specific marketplaces (e.g., Kaufland, Cdiscount, eBay). You can customize and extend these rulesets to suit the guidelines of other marketplaces or to add more detail to the generation process.

Please note that the provided code is a basic implementation and may require additional configuration and security measures for a production environment.

For more details on the code and how to customize it for your specific use case, refer to the code comments and documentation in the respective files.
