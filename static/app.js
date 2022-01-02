const BASE_URL = "http://localhost:5000/api";

function createCupcakeHTML (cupcake) {
    return `
    <div class = "cupcake-child-container" id=${cupcake.id}>
        <a href = "/${cupcake.id}">
        <img src = "${cupcake.image}">
        <p>${cupcake.flavor}</a></p>
        <p>Size: ${cupcake.size}</p>
        <p>Rating: ${cupcake.rating}</p>
        <button id = "delete">Delete</button>
    </div>    
    `;
}


async function displayCupcakes() {
    const resp = await axios.get(`${BASE_URL}/cupcakes`)

    for (let cupcakeData of resp.data.cupcakes) {
        let newCupcake = $(createCupcakeHTML(cupcakeData))
        $(".cupcake-display-container").append(newCupcake)
    }
}


$("form").submit( async function (evt) {
    evt.preventDefault();

    let flavor = $("#flavor").val();
    let rating = $("#rating").val();
    let size = $("#size").val();
    let image = $("#image").val();

    const newCupcakeRes = await axios.post(`api/cupcakes`, {
        "flavor": flavor,
        "rating": rating,
        "size": size,
        "image": image
    });

    let newCupcake = $(createCupcakeHTML(newCupcakeRes.data.cupcake));
    $(".cupcake-display-container").append(newCupcake);    
    $("form").trigger("reset");
})

$(".cupcake-display-container").on("click", "#delete", async function (evt) {
    evt.preventDefault();
    let $cupcake = $(evt.target).parent()
    let cupcakeId = $cupcake.attr("id")

    await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`)
    $cupcake.remove();
})

displayCupcakes();