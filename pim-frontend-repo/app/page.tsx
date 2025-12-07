"use client"; // 1. Esto avisa a Next.js que esta página usa interactividad (clicks, inputs)

import { useState } from "react";
import { useRouter } from "next/navigation"; // Para cambiar de página al loguearse

export default function LoginPage() {
  const router = useRouter();
  
  // 2. Estados para guardar lo que escribe el usuario
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  // 3. Función que se ejecuta al dar click en "Ingresar"
  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(""); // Limpiamos errores previos

    try {
      // A. Enviamos los datos a TU backend (puerto 8000)
      const res = await fetch("http://127.0.0.1:8000/api/v1/auth/token", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        // El formato OAuth2 pide los datos así:
        body: new URLSearchParams({
          username: username,
          password: password,
        }),
      });

      // B. Si falla (ej: contraseña mal), mostramos error
      if (!res.ok) {
        throw new Error("Usuario o contraseña incorrectos");
      }

      // C. Si todo bien, guardamos el token
      const data = await res.json();
      localStorage.setItem("pim_token", data.access_token); // Guardar en el navegador
      
      //alert("¡Login Exitoso! Token guardado.");
     
      router.push("/dashboard"); 

    } catch (err: any) {
      setError(err.message);
    }
  };

  // 4. El HTML (JSX) de la página
  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-100">
      <div className="w-full max-w-md bg-white p-8 rounded-lg shadow-md">
        
        <h1 className="text-2xl font-bold text-center text-gray-800 mb-6">
          PIM Centroamérica
        </h1>

        <form onSubmit={handleLogin} className="space-y-4">
          
          {/* Campo Usuario */}
          <div>
            <label className="block text-sm font-medium text-gray-700">Usuario</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 text-black"
              placeholder="admin"
              required
            />
          </div>

          {/* Campo Contraseña */}
          <div>
            <label className="block text-sm font-medium text-gray-700">Contraseña</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 text-black"
              placeholder="••••••"
              required
            />
          </div>

          {/* Mensaje de Error (si existe) */}
          {error && (
            <div className="text-red-500 text-sm text-center font-medium">
              {error}
            </div>
          )}

          {/* Botón */}
          <button
            type="submit"
            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Ingresar
          </button>
        </form>
      </div>
    </div>
  );
}