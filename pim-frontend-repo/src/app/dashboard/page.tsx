"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

// Definimos los tipos de datos (Interfaces)
interface Variant {
  color: string;
  stock_quantity: number;
  price: number;
}

interface Product {
  id: number;
  sku: string;
  name: string; // Este nombre cambiará según el país (Tropicalización)
  category: string;
  variants: Variant[];
  images?: any[];
}

export default function Dashboard() {
  const router = useRouter();
  const [products, setProducts] = useState<Product[]>([]);
  const [country, setCountry] = useState("GT"); // Por defecto Guatemala
  const [loading, setLoading] = useState(true);

  // Función para cargar productos desde tu API
  const fetchProducts = async (selectedCountry: string) => {
    setLoading(true);
    // Recuperamos el token que guardamos en el Login
    const token = localStorage.getItem("pim_token");

    if (!token) {
      router.push("/"); // Si no hay token, mandar al login
      return;
    }

    try {
      // Llamamos al Backend enviando el token y el país
      const res = await fetch(`http://127.0.0.1:8000/api/v1/products/?country_code=${selectedCountry}`, {
        headers: {
          Authorization: `Bearer ${token}`, // Aquí va tu pase VIP
        },
      });

      if (res.status === 401) {
        alert("Tu sesión expiró");
        router.push("/");
        return;
      }

      const data = await res.json();
      setProducts(data);
    } catch (error) {
      console.error("Error cargando productos:", error);
    } finally {
      setLoading(false);
    }
  };

  // Cargar productos al iniciar o al cambiar el país
  useEffect(() => {
    fetchProducts(country);
  }, [country]);

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      {/* Encabezado */}
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-800">📦 PIM Dashboard</h1>
        
        {/* Selector de Tropicalización */}
        <div className="flex items-center gap-4">
          <span className="text-gray-600 font-medium">Ver como:</span>
          <select 
            value={country} 
            onChange={(e) => setCountry(e.target.value)}
            className="p-2 border rounded bg-white text-gray-800 shadow-sm"
          >
            <option value="GT">🇬🇹 Guatemala</option>
            <option value="SV">🇸🇻 El Salvador</option>
            <option value="HN">🇭🇳 Honduras</option>
          </select>
          
          <button 
            onClick={() => {
              localStorage.removeItem("pim_token");
              router.push("/");
            }}
            className="ml-4 px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
          >
            Salir
          </button>
        </div>
      </div>

      {/* Tabla de Productos */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-100">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider text-black">SKU</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider text-black">Nombre (Tropicalizado)</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider text-black">Categoría</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider text-black">Variantes (Stock)</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {loading ? (
              <tr><td colSpan={4} className="p-8 text-center text-gray-500">Cargando productos...</td></tr>
            ) : products.map((product) => (
              <tr key={product.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap font-mono text-sm text-blue-600">{product.sku}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-bold text-gray-900">
                  {product.name} 
                  {/* Etiqueta visual para confirmar que cambió */}
                  <span className="ml-2 text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full">
                    {country}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{product.category}</td>
                <td className="px-6 py-4 text-sm text-gray-500">
                  {product.variants.map((v, idx) => (
                    <div key={idx} className="mb-1">
                      <span className="font-medium text-gray-700">{v.color}:</span> {v.stock_quantity} unds (Q{v.price})
                    </div>
                  ))}
                  {product.variants.length === 0 && <span className="text-gray-400 italic">Sin variantes</span>}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
