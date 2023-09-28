; (function() {
    const modal = new bootstrap.Modal(document.getElementById('modal'))

    document.body.addEventListener('htmx:afterSwap', (e) => {
        if (e.detail.target.id === "dialog")
        modal.show()
    })
})()