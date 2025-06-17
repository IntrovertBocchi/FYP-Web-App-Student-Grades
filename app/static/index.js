let currentChartType = 'precision-recall';
let chartInstance = null;
let storedAccuracyData = null;
let storedConfMatrix = null;
let showingHeatmap = false;

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
      <label>CLA Scores (10): <input type="number" id="cla_scores" max="10" step="0.01" min="0"/></label>
      <label>Quiz Scores (15):<input type="number" id="quiz_scores" max="15" step="0.01" min="0"/></label>
    `;
    
    // Enforce decimal limit on all inputs
    ['report_a', 'report_b', 'group_exercise', 'cla_scores', 'quiz_scores'].forEach(id => {
      const input = document.getElementById(id);
      if (input) enforceTwoDecimalPlaces(input);
    });

  } else if (program === 'COS') {

    container.innerHTML = `
      <label>Lab Exercise (10): <input type="number" id="lab_exercises" max="10" step="0.01" min="0"/></label>
      <label>Assignment 1 (100): <input type="number" id="assignment1" max="100" step="0.01" min="0"/></label>
      <label>Assignment 2 (100): <input type="number" id="assignment2" max="100" step="0.01" min="0"/></label>
      <label>Midterm (35): <input type="number" id="midterm" max="35" step="0.01" min="0"/></label>
    `;

    // Enforce decimal limit on all inputs
    ['lab_exercises', 'assignment1', 'assignment2', 'midterm'].forEach(id => {
      const input = document.getElementById(id);
      if (input) enforceTwoDecimalPlaces(input);
    });

  } else if (program === 'ADV') {

     container.innerHTML = `
      <label>Quiz Scores (20): <input type="number" id="quiz_scores" max="20" step="0.01" min="0"/></label>
      <label>Assignment 1 (10): <input type="number" id="assignment1" max="10" step="0.01" min="0"/></label>
      <label>Assignment 2 (40): <input type="number" id="assignment2" max="40" step="0.01" min="0"/></label>
      <label>OBOW Test (30): <input type="number" id="obow_test" max="30" step="0.01" min="0"/></label>
    `;

    // Enforce decimal limit on all inputs
    ['quiz_scores', 'assignment1', 'assignment2', 'obow_test'].forEach(id => {
      const input = document.getElementById(id);
      if (input) enforceTwoDecimalPlaces(input);
    });

  }

}

async function calculateGrade() {
  const program = document.getElementById('program').value;

  // Fill all empty inputs to 0 before proceeding
  fillEmptyInputsToZero();
  
  let inputs = {};
  let fallbackResult = '';
  let endpointInputs = {};

  if (program === 'INF') {

    inputs = {
      report_a: parseFloat(document.getElementById('report_a').value),
      report_b: parseFloat(document.getElementById('report_b').value),
      group_exercise: parseFloat(document.getElementById('group_exercise').value),
      cla_scores: parseFloat(document.getElementById('cla_scores').value),
      quiz_scores: parseFloat(document.getElementById('quiz_scores').value)

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

      lab_exercises: parseFloat(document.getElementById('lab_exercises').value),
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
      quiz_scores: parseFloat(document.getElementById('quiz_scores').value),
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
       showGrade(result.predicted_score, result.passing_guidance);
    } else {
      const errorMessage = result?.error || "Unexpected backend error";
      console.error("Backend error:", errorMessage);
      showGrade(fallbackResult);
    }
  } catch (err) {
    console.error("Fetch failed:", err);
    showGrade(fallbackResult);
  }  
}



function showGrade(score, guidance = null) {

  let grade = '';
  const percentage = parseFloat(score);

  if (percentage >= 80) grade = 'HD';
  
  else if (percentage >= 70) grade = 'D';

  else if (percentage >= 60) grade = 'C';
  
  else if (percentage >= 50) grade = 'P';
  
  else grade = 'F';
  
  
  let resultText = `
    Score: ${percentage.toFixed(2)}%
    Grade: ${grade}
  `;

  if (guidance) {
    resultText += `\n\n📌 Passing Guidance:\n${guidance}`;
  }

  document.getElementById('result').innerText = resultText;
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
      if (data.error) throw new Error(data.error);

      storedAccuracyData = data;
      document.getElementById('accuracy-text').innerText = `Overall Accuracy: ${(data.accuracy * 100).toFixed(2)}%`;
      drawAccuracyChart();

    })

    .catch(error => {
      document.getElementById('accuracy-text').innerText = "⚠️ Failed to load model accuracy.";
      console.error("Accuracy fetch error:", error);
    });
  
  // Preload confusion matrix    
  fetch('/api/confusion_matrix')
    .then(response => response.json())
    .then(data => {
      if (!data.error) {
        storedConfMatrix = data;
      }
    })
    .catch(err => console.error("Confusion matrix fetch failed:", err));
}

function drawAccuracyChart() {

  if (!storedAccuracyData) {
    console.warn("No accuracy data.");
    return;
  }

  const canvas = document.getElementById('accuracy-chart');
  if (!canvas) {
    console.error("Canvas element #accuracy-chart not found!");
    return;
  }

  const ctx = canvas.getContext('2d');
  const details = storedAccuracyData.details;

  const labels = Object.keys(details);
  const precisions = labels.map(label => details[label].precision * 100);
  const recalls = labels.map(label => details[label].recall * 100);


  if (chartInstance) chartInstance.destroy();

  chartInstance = new Chart(ctx, {
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
      },
      plugins: {
        legend: { position: 'top' },
        title: { display: true, text: 'Model Precision and Recall by Grade' }
      }
    }
  });
}



function drawConfusionMatrixChart() {
  if (!storedConfMatrix) return;

  const labels = storedConfMatrix.labels;
  const matrix = storedConfMatrix.matrix;

  const ctx = document.getElementById('accuracy-chart').getContext('2d');
  if (chartInstance) chartInstance.destroy();

  chartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: labels.map((actualLabel, i) => ({
        label: `Actual ${actualLabel}`,
        data: matrix[i],
        backgroundColor: `hsl(${(i * 60) % 360}, 70%, 60%)`
      }))
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'top' },
        title: { display: true, text: 'Confusion Matrix (Predicted Counts by Actual Grade)' }
      },
      scales: {
        x: { stacked: true },
        y: { stacked: true, beginAtZero: true }
      }
    }
  });
}

function toggleHeatmap() {
  if (!storedConfMatrix) return;

  const labels = storedConfMatrix.labels;
  const matrix = storedConfMatrix.matrix;

  const ctx = document.getElementById('accuracy-chart').getContext('2d');
  if (chartInstance) chartInstance.destroy();

  if (!showingHeatmap) {
    // Show heatmap
    chartInstance = new Chart(ctx, {
      type: 'matrix',
      data: {
        labels: labels,
        datasets: [{
          label: 'Confusion Matrix Heatmap',
          data: matrix.flatMap((row, rowIndex) =>
            row.map((value, colIndex) => ({
              x: labels[colIndex],
              y: labels[rowIndex],
              v: value
            }))
          ),
          backgroundColor(ctx) {
            const value = ctx.dataset.data[ctx.dataIndex].v;
            const max = Math.max(...matrix.flat());
            const intensity = value / max;
            return `rgba(255, 99, 132, ${intensity})`;
          },
          width: ({ chart }) => (chart.chartArea || {}).width / labels.length - 2,
          height: ({ chart }) => (chart.chartArea || {}).height / labels.length - 2
        }]
      },
      options: {
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              title: () => '',
              label: ctx => `Actual: ${ctx.raw.y}, Predicted: ${ctx.raw.x}, Count: ${ctx.raw.v}`
            }
          },
          title: {
            display: true,
            text: 'Confusion Matrix Heatmap'
          }
        },
        scales: {
          x: { type: 'category', title: { display: true, text: 'Predicted' } },
          y: { type: 'category', title: { display: true, text: 'Actual' } }
        }
      }
    });

    // Update state and button
    showingHeatmap = true;
    document.getElementById('heatmap-btn').innerText = "👁️ View Stacked Bar";

  } else {
    // Show stacked bar again
    drawConfusionMatrixChart();
    showingHeatmap = false;
    document.getElementById('heatmap-btn').innerText = "👁️ View Heatmap";
  }
}


function toggleChart() {
  
  if (currentChartType === 'precision-recall') {

    drawConfusionMatrixChart();
    currentChartType = 'confusion-matrix';
    document.getElementById('heatmap-btn').style.display = 'inline-block';
    document.getElementById('heatmap-btn').innerText = "👁️ View Heatmap";
    showingHeatmap = false; // reset when switching back
  } else {
    drawAccuracyChart();
    currentChartType = 'precision-recall';
    document.getElementById('heatmap-btn').style.display = 'none';
    showingHeatmap = false; // reset when switching back
  }
}

// Toggle and check password
document.addEventListener("DOMContentLoaded", function () {
  const toggles = document.querySelectorAll(".toggle-password");

  toggles.forEach(toggle => {
    toggle.addEventListener("click", function () {
      const targetId = this.getAttribute("data-target");
      const input = document.getElementById(targetId);

      if (input) {
        const isPassword = input.getAttribute("type") === "password";
        input.setAttribute("type", isPassword ? "text" : "password");

        // Toggle icon
        this.classList.toggle("bi-eye-slash");
        this.classList.toggle("bi-eye");
      }
    });
  });
});

// Utility function to fill empty fields
function fillEmptyInputsToZero() {
  const inputs = document.querySelectorAll('#dynamic-fields input[type="number"]');
  let anyFilled = false;

  inputs.forEach(input => {
    if (input.value.trim() === '') {
      input.value = '0';
      anyFilled = true;
    }
  });

  if (anyFilled) {
    showTemporaryAlert("Empty fields have been auto-filled with 0.");
  }
}

// Temporary alert function
function showTemporaryAlert(message) {
  const alertBox = document.createElement('div');
  alertBox.className = 'temp-alert';
  alertBox.innerText = message;

  document.body.appendChild(alertBox);

  setTimeout(() => {
    alertBox.remove();
  }, 2500); // disappears after 2.5 seconds
}


// Call on page load
document.addEventListener("DOMContentLoaded", loadModelAccuracy);


