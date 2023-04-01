import axios from "axios";

let local = "http://localhost:8000/api/v1/"
let azure = "https://ta-scheduling.azurewebsites.net/api/v1/"

export default axios.create({
    baseURL: azure,
    headers:{
        "Content-type": "application/json"
    }
});