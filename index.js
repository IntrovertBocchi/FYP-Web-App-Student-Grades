function calculateGrade() {
  const age = parseFloat(document.getElementById('age').value);
  const attendance = parseFloat(document.getElementById('attendance').value);
  const sleepinghours = parseFloat(document.getElementById('sleepinghours').value);
  const studyhours = parseFloat(document.getElementById('studyhours').value);


  if (isNaN(age) || isNaN(attendance) || isNaN(sleepinghours) || isNaN(studyhours)) {
    document.getElementById('result').innerText = 'Please enter valid marks for all subjects.';
    return;
  }

  if (age < 0 || attendance < 0 || sleepinghours < 0 || studyhours < 0){
    document.getElementById('result').innerText= 'Marks should not be below 0. Please check again.';
    return; 
  }

  const total = age + attendance + sleepinghours + studyhours;
  const percentage = (total / 400) * 100;
  let grade = '';

  if (percentage >= 90) {
    grade = 'A';
  } else if (percentage >= 80) {
    grade = 'B';
  } else if (percentage >= 70) {
    grade = 'C';
  } else if (percentage >= 60) {
    grade = 'D';
  } else {
    grade = 'F';
  }

  document.getElementById('result').innerText = `Total Scores: ${total}/400
Percentage: ${percentage.toFixed(2)}%
Grade: ${grade}`;
}
