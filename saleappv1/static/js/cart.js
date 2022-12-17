function addToCart(macb, ngaygio, thoigianbay, gia) {
    fetch('/api/cart', {
        method: "post",
        body: JSON.stringify({
            "macb": macb,
            "ngaygio": ngaygio,
            "thoigianbay":thoigianbay,
            "giave": gia
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        console.info(data)
        let d = document.getElementsByClassName("cart-counter")
        for (let i = 0; i < d.length; i++)
            d[i].innerText = data.total_quantity
    }) // js promise
}