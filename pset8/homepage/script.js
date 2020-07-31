function hello()
{
    sessionStorage.setItem("background", document.querySelector("#Background").value);
    sessionStorage.setItem("aims", document.querySelector("#Aims").value);
    sessionStorage.setItem("results", document.querySelector("#Results").value);
    sessionStorage.setItem("conclusion", document.querySelector("#Conclusion").value);
}