
avaluoBien.addEventListener("change", function () {
    const filePath = this.value.replace(/C:\\fakepath\\/i, "");
    document.getElementById("displayFilePath").innerText = filePath;
});