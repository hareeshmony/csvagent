import os
import json
from groq import Groq
from pydantic import BaseModel, Field, ValidationError # pip install pydantic
from typing import List

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Define a schema with Pydantic (Python's equivalent to Zod)
class Product(BaseModel):
    html_content: str
    summary: str
    
# Prompt design is critical for structured outputs
system_prompt = """
You are a data summary & data visualizing expert. You will be shown the Users question & the csv agent's output, \
You should summarize the agents results and also plot the data with a suitable plot technique via HTML format doc content.
html_content --> used for either plots or tables, default value is ""
summary --> used for summarizing the result in a report fashion
Note: always respond with valid JSON objects that match this complete HTML structure while plotting
If the data is Not plottable, return default empty str as output in place of html_content.
Example:
{
  "html_content": "
  <!DOCTYPE html>
<html>
<head>
  <title>Category Data Visualization</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 40px;
    }

    .container {
      display: flex;
      gap: 40px;
      align-items: flex-start;
    }

    table {
      border-collapse: collapse;
      width: 300px;
    }

    th, td {
      border: 1px solid #ccc;
      padding: 12px;
      text-align: center;
    }

    th {
      background-color: #f4f4f4;
    }

    .chart-container {
      width: 400px;
    }
  </style>
</head>
<body>

  <h2>Category Distribution</h2>

  <div class="container">
    <!-- Table -->
    <table>
      <thead>
        <tr>
          <th>Category</th>
          <th>Percentage</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Category 1</td>
          <td>20%</td>
        </tr>
        <tr>
          <td>Category 2</td>
          <td>80%</td>
        </tr>
      </tbody>
    </table>

    <!-- Pie Chart -->
    <div class="chart-container">
      <canvas id="categoryChart"></canvas>
    </div>
  </div>

  <script>
    const ctx = document.getElementById('categoryChart').getContext('2d');
    const categoryChart = new Chart(ctx, {
      type: 'pie',
      data: {
        labels: ['Category 1', 'Category 2'],
        datasets: [{
          label: 'Category Distribution',
          data: [20, 80],
          backgroundColor: ['#4e79a7', '#f28e2b']
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'bottom'
          }
        }
      }
    });
  </script>

</body>
</html>

",
  "summary": 
  "Category 1 accounts for 20% of the total.
   Category 2 dominates with 80% of the total."
}
Your response should ONLY contain the JSON object and nothing else.
"""

def output_formatter(user_question, csv_agent_response):
  # Request structured data from the model
  completion = client.chat.completions.create(
      model="llama-3.3-70b-versatile",
      response_format={"type": "json_object"},
      messages=[
          {"role": "system", "content": system_prompt},
          {"role": "user", "content": f" user question: {user_question},\ncsv agent output:{csv_agent_response}"}
      ]
  )

  # Extract and validate the response
  try:
      response_content = completion.choices[0].message.content
      json_data        = json.loads(response_content)
      product          = Product(**json_data)
      print("Validation successful! Structured data:", json_data)
      print("\nPlot Validation successful!")

      return product.html_content, product.summary
  except json.JSONDecodeError:
      print("Error: The model did not return valid JSON")
  except ValidationError as e:
      print(f"Error: The JSON did not match the expected schema: {e}") 