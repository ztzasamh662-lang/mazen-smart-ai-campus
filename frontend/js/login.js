function login(){

const role = document.getElementById("role").value
const username = document.getElementById("username").value.trim()

if(username === ""){
alert("Please enter your name")
return
}

localStorage.setItem("role",role)
localStorage.setItem("username",username)

if(role === "admin"){
window.location.href="index.html"
}else{
window.location.href="student.html"
}

}