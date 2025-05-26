const fieldLabels = {
  report_a: "Report A",
  report_b: "Report B",
  group_exercise: "Group Exercise",
  cla_scores: "CLA Score",
  quiz_scores: "Quiz Score",
  lab_exercises: "Lab Exercise",
  assignment1: "Assignment 1",
  assignment2: "Assignment 2",
  midterm: "Midterm",
  obow_test: "OBOW Test"
};


function validateInputs(inputs, maxes) {
  const errors = [];

  for (let key in inputs) {
    let value = inputs[key];
    const max = maxes[key];
    const label = fieldLabels[key] || key;

    if (Array.isArray(value)) {
      for (let i = 0; i < value.length; i++) {
        value[i] = Math.round(value[i] * 100) / 100;
        if (isNaN(value[i]) || value[i] < 0 || value[i] > max[i]) {
          errors.push(`${label} must be between 0 and ${max[i]}`);
        }
      }
    } else {
      value = Math.round(value * 100) / 100;
      if (isNaN(value) || value < 0 || value > max) {
        errors.push(`${label} must be between 0 and ${max}`);
      }
    }
  }

  if (errors.length > 0) {
    return errors.join('\n');
  }

  return null;
}

function showfields() {
  const program = document.getElementById('program').value;
  const container = document.getElementById('dynamic-fields');
  container.innerHTML = ''; //Clear previous fields
  document.getElementById('result').innerText = ''; //Clear previous results

  if (program === 'INF') {

    container.innerHTML = `
      <label>Report A (25): <input type="number" id="report_a" max="25" step="0.01" min="0"/></label>
      <label>Report B (20): <input type="number" id="report_b" max="20" step="0.01" min="0"/></label>
      <label>Group Exercise (5): <input type="number" id="group_exercise" max="5" step="0.01" min="0"/></label>
      <label>CLA Scores (10): <input type="number" id="cla" max="10" step="0.01" min="0"/></label>
      <label>Quiz Scores (15):<input type="number" id="quiz" max="15" step="0.01" min="0"/></label>
    `;
    
    // Enforce decimal limit on all inputs
    ['report_a', 'report_b', 'group_exercise', 'cla', 'quiz'].forEach(id => {
      const input = document.getElementById(id);
      if (input) enforceTwoDecimalPlaces(input);
    });

  } else if (program === 'COS') {

    container.innerHTML = `
      <label>Lab Exercise (10): <input type="number" id="lab_total" max="10" step="0.01" min="0"/></label>
      <label>Assignment 1 (100): <input type="number" id="assignment1" max="100" step="0.01" min="0"/></label>
      <label>Assignment 2 (100): <input type="number" id="assignment2" max="100" step="0.01" min="0"/></label>
      <label>Midterm (35): <input type="number" id="midterm" max="35" step="0.01" min="0"/></label>
    `;

    // Enforce decimal limit on all inputs
    ['lab_total', 'assignment1', 'assignment2', 'midterm'].forEach(id => {
      const input = document.getElementById(id);
      if (input) enforceTwoDecimalPlaces(input);
    });

  } else if (program === 'ADV') {

     container.innerHTML = `
      <label>Quiz Scores (20): <input type="number" id="quiz" max="20" step="0.01" min="0"/></label>
      <label>Assignment 1 (10): <input type="number" id="assignment1" max="10" step="0.01" min="0"/></label>
      <label>Assignment 2 (40): <input type="number" id="assignment2" max="40" step="0.01" min="0"/></label>
      <label>OBOW Test (30): <input type="number" id="obow_test" max="30" step="0.01" min="0"/></label>
    `;

    // Enforce decimal limit on all inputs
    ['quiz', 'assignment1', 'assignment2', 'obow_test'].forEach(id => {
      const input = document.getElementById(id);
      if (input) enforceTwoDecimalPlaces(input);
    });

  }

}

async function calculateGrade() {
  const program = document.getElementById('program').value;
  let inputs = {};
  let fallbackResult = '';
  let endpointInputs = {};

  if (program === 'INF') {

    inputs = {
      report_a: parseFloat(document.getElementById('report_a').value),
      report_b: parseFloat(document.getElementById('report_b').value),
      group_exercise: parseFloat(document.getElementById('group_exercise').value),
      cla_scores: parseFloat(document.getElementById('cla').value),
      quiz_scores: parseFloat(document.getElementById('quiz').value)

    };

    const maxes = {
      report_a: 25,
      report_b: 20,
      group_exercise: 5,
      cla_scores: 10,
      quiz_scores: 15
    }

    const error = validateInputs(inputs, maxes);
      if (error) {
      document.getElementById('result').innerText = error;
      return;
    }

    fallbackResult = (
      (inputs.report_a / 25) * 25 +
      (inputs.report_b / 20) * 20 +
      (inputs.group_exercise / 5) * 5 +
      (inputs.cla_scores / 10) * 30 +
      (inputs.quiz_scores / 15) * 20
    );

    endpointInputs = inputs;

  } else if (program === 'COS') {

    inputs = {

      lab_exercises: parseFloat(document.getElementById('lab_total').value),
      assignment1: parseFloat(document.getElementById('assignment1').value),
      assignment2: parseFloat(document.getElementById('assignment2').value),
      midterm: parseFloat(document.getElementById('midterm').value),

    };

    const maxes = {
      lab_exercises: 10,
      assignment1: 100,
      assignment2: 100,
      midterm: 35
    };

    const error = validateInputs(inputs, maxes);
    if (error) {
      document.getElementById('result').innerText = error;
      return;
    }

    fallbackResult = (

      (inputs.lab_exercises / 10) * 10 +
      (inputs.assignment1 / 100) * 30 +
      (inputs.assignment2 / 100) * 40 +
      (inputs.midterm / 35) * 20

    );

    endpointInputs = inputs;

  } else if (program === 'ADV') {

    inputs = {
      quiz_scores: parseFloat(document.getElementById('quiz').value),
      assignment1: parseFloat(document.getElementById('assignment1').value),
      assignment2: parseFloat(document.getElementById('assignment2').value),
      obow_test: parseFloat(document.getElementById('obow_test').value),
    };
    
    const maxes = {
      quiz_scores: 20,
      assignment1: 10,
      assignment2: 40,
      obow_test: 30
    };

    const error = validateInputs(inputs, maxes);
    if (error) {
      document.getElementById('result').innerText = error;
      return;
    }
    
    fallbackResult = (

      (inputs.quiz_scores / 20) * 20 +
      (inputs.assignment1 / 10) * 10 +
      (inputs.assignment2 / 40) * 40 +
      (inputs.obow_test / 30) * 30

    );

    endpointInputs = inputs;

  } else {
    document.getElementById('result').innerText = 'Please select a program.';
    return;
  }

  //Call Flask backend
  try {
    
    const response = await fetch('/api/predict', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        subject: program,
        inputs: endpointInputs,
      })
    });

    const result = await response.json();

    if (response.ok) {
      showGrade(result.score);
    } else {
      const errorMessage = result?.error || "Unexpected backend error";
      //console.error("Backend error:", errorMessage);
      showGrade(fallbackResult);
    }
  } catch (err) {
    //console.error("Fetch failed:", err);
    showGrade(fallbackResult);
  }  
}



function showGrade(score) {

  let grade = '';
  const percentage = parseFloat(score);

  if (percentage >= 80) grade = 'HD';
  
  else if (percentage >= 70) grade = 'D';

  else if (percentage >= 60) grade = 'C';
  
  else if (percentage >= 50) grade = 'P';
  
  else grade = 'F';
  
  
  document.getElementById('result').innerText = `
    Score: ${percentage.toFixed(2)}%
    Grade: ${grade}
  `;
 
}


function enforceTwoDecimalPlaces(input) {
  input.addEventListener('input', () => {
    const value = input.value;
    if (value.includes('.')) {
      const parts = value.split('.');
      if (parts[1].length > 2) {
        input.value = `${parts[0]}.${parts[1].slice(0, 2)}`;
      }
    }
  });
}

// Fetch and display model accuracy
function loadModelAccuracy() {
  fetch('/api/accuracy')
    .then(response => response.json())
    .then(data => {
      const accuracy = data.accuracy;
      document.getElementById('accuracy-text').innerText = `Overall Accuracy: ${(accuracy * 100).toFixed(2)}%`;

      const labels = Object.keys(data.details);
      const precisions = labels.map(label => data.details[label].precision * 100);
      const recalls = labels.map(label => data.details[label].recall * 100);

      const ctx = document.getElementById('accuracy-chart').getContext('2d');
      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Precision (%)',
              backgroundColor: '#28a745',
              data: precisions
            },
            {
              label: 'Recall (%)',
              backgroundColor: '#17a2b8',
              data: recalls
            }
          ]
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              max: 100
            }
          }
        }
      });
    })
    .catch(error => {
      document.getElementById('accuracy-text').innerText = "Failed to load model accuracy.";
      console.error("Accuracy fetch error:", error);
    });
}

// Call it on page load
document.addEventListener("DOMContentLoaded", function () {
  loadModelAccuracy();
});
