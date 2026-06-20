import React, { useState } from "react";
import "./Register.css";

export default function Register() {
  const [form, setForm] = useState({ username: "", firstName: "", lastName: "", email: "", password: "" });
  const change = ({ target }) => setForm({ ...form, [target.name]: target.value });
  const submit = async (event) => {
    event.preventDefault();
    await fetch("/djangoapp/register", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(form) });
  };
  return <main className="register-page"><form onSubmit={submit}>
    <h1>Create your RoadStar account</h1>
    <label>Username<input name="username" value={form.username} onChange={change} required /></label>
    <label>First Name<input name="firstName" value={form.firstName} onChange={change} required /></label>
    <label>Last Name<input name="lastName" value={form.lastName} onChange={change} required /></label>
    <label>Email<input name="email" type="email" value={form.email} onChange={change} required /></label>
    <label>Password<input name="password" type="password" value={form.password} onChange={change} required /></label>
    <button type="submit">Register</button>
  </form></main>;
}

