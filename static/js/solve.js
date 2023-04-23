document
  .getElementById("sender")
  .addEventListener("submit", async function (e) {
    e.preventDefault();
    let data = new FormData();
    let arr = [];
    for (let a = 0; a < 9; a++) {
      let row = [];
      for (let b = 0; b < 9; b++) {
        let element = a + " " + b;
        let val = document.getElementById(element).value;
        if (val == "") {
          val = 0;
        }
        row.push(parseInt(val));
      }
      arr.push(row);
    }
    data.append("photo", window.location.search.substring(1));
    data.append("table", JSON.stringify(arr));
    await fetch("/solve", {
      method: "POST",
      body: data,
    })
      .then(async (response) => {
        if (response.ok) {
          await response.json().then((data) => {
            window.location.href = "/solve?p=" + data.id;
          });
        } else {
          throw new Error("Something went wrong ...");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  });
