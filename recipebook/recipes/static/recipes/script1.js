function addIngredient() {
    const input = document.getElementById("ingredientInput");
    const value = input.value.trim();
  
    if (value) {
        fetch("/add_ingredient/", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCSRFToken(),
            },
            body: "name=" + encodeURIComponent(value),
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            loadIngredients();
            input.value = "";
        });
    }
}

function deleteIngredient(name) {
    fetch("/delete_ingredient/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCSRFToken(),
        },
        body: "name=" + encodeURIComponent(name),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
        loadIngredients(); // ✅ Refresh the list after deletion
    });
}

function loadIngredients() {
    fetch("/get_ingredients/")
    .then(response => response.json())
    .then(data => {
        const list = document.getElementById("ingredientList");
        list.innerHTML = "";
        data.ingredients.forEach((item) => {
            const li = document.createElement("li");
            li.textContent = item;

            // ✅ Add Delete Button
            const btn = document.createElement("button");
            btn.textContent = "X";
            btn.classList.add("delete-btn"); // Optional styling
            btn.onclick = () => deleteIngredient(item); // ✅ Send ingredient name

            li.appendChild(btn);
            list.appendChild(li);
        });
    });
}

function getFinalSuggestions() {
    const commonFoods = {
        banana: "Banana smoothie",
        broccoli: "Steamed broccoli",
        oats: "Oats bowl",
        cucumber: "Cucumber salad",
        quinoa: "Quinoa with stir-fried veggies",
        apple: "Apple slices with peanut butter"
    };

    fetch("/get_ingredients/")
    .then(response => response.json())
    .then(data => {
        let matches = data.ingredients
            .map(ing => ing.toLowerCase())
            .map(ing => commonFoods[ing])
            .filter(Boolean);

        if (matches.length === 0) {
            matches = ["Try adding more healthy ingredients!"];
        }

        document.getElementById("finalSuggestions").innerHTML =
            "<strong>Suggestions Based on Ingredients:</strong> <ul>" +
            matches.map(item => `<li>${item}</li>`).join('') + "</ul>";
    });
}

function getCSRFToken() {
    return document.querySelector("[name=csrfmiddlewaretoken]").value;
}

document.addEventListener("DOMContentLoaded", loadIngredients);
