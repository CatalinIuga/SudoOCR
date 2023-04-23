function checkSudoku() {
  let grid = Array(9)
    .fill()
    .map(() => Array(9).fill(0));
  for (var a = 0; a < 9; a++) {
    for (var b = 0; b < 9; b++) {
      if (document.getElementById(a + " " + b).value) {
        grid[a][b] = document.getElementById(a + " " + b).value;
      } else {
        grid[a][b] = 0;
      }
    }
  }

  let valid = true;
  // check rows
  grid.forEach((line) => {
    // check duplicates
    aux = line.filter((x) => x != 0);
    check = new Set(aux);

    if (check.size !== aux.length) {
      valid = false;
    }
  });
  // check columns
  for (var i = 0; i < 9; i++) {
    aux = [];
    for (var j = 0; j < 9; j++) {
      if (grid[j][i] != 0) aux.push(grid[j][i]);
    }
    check = new Set(aux.filter((x) => x != 0));
    if (check.size != aux.filter((x) => x != 0).length) {
      valid = false;
    }
  }

  // check squares
  for (var i = 0; i < 9; i += 3) {
    for (var j = 0; j < 9; j += 3) {
      aux = [];
      for (var k = 0; k < 3; k++) {
        for (var l = 0; l < 3; l++) {
          if (grid[i + k][j + l] != 0) aux.push(grid[i + k][j + l]);
        }
      }
      check = new Set(aux.filter((x) => x != 0));
      if (check.size != aux.filter((x) => x != 0).length) {
        valid = false;
        break;
      }
    }
  }

  let button = document.getElementById("checked");
  if (!valid) {
    button.disabled = true;
    button.classList.add("bg-red-500");
    button.classList.remove("bg-green-500");
    button.innerHTML = "Not solvable";
    return;
  }
  button.disabled = false;
  button.classList.remove("bg-red-500");
  button.classList.add("bg-green-500");
  button.innerHTML = "Solve";
}
checkSudoku();
