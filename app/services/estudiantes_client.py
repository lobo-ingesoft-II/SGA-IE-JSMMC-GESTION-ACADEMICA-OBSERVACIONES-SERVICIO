import httpx
from typing import Optional, Dict, Any
from app.config import settings
import asyncio
from fastapi import HTTPException

class EstudiantesClient:
    def __init__(self):
        self.base_url = getattr(settings, 'ESTUDIANTES_API_URL', 'http://localhost:8005')
        self.timeout = httpx.Timeout(10.0, connect=5.0)
        self.client = httpx.AsyncClient(timeout=self.timeout)
        self.max_retries = 3
        self.retry_delay = 1.0
    
    async def _make_request_with_retry(self, method: str, url: str, **kwargs) -> Optional[httpx.Response]:
        """
        Realiza una petición HTTP con reintentos automáticos
        """
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                response = await self.client.request(method, url, **kwargs)
                return response
            except (httpx.ConnectError, httpx.TimeoutException, httpx.RequestError) as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay * (2 ** attempt))  # Backoff exponencial
                continue
        
        # Si llegamos aquí, todos los reintentos fallaron
        raise HTTPException(
            status_code=503,
            detail=f"Servicio de estudiantes no disponible: {str(last_exception)}"
        )
    
    async def get_estudiante_info(self, id_estudiante: int) -> Optional[Dict[str, Any]]:
        """
        Obtiene información completa del estudiante desde la API de estudiantes
        """
        try:
            response = await self._make_request_with_retry(
                "GET", 
                f"{self.base_url}/estudiantes/{id_estudiante}"
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return None
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Error al obtener estudiante: {response.text}"
                )
                
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error interno al consultar estudiante {id_estudiante}: {str(e)}"
            )
    
    async def verificar_estudiante_existe(self, id_estudiante: int) -> bool:
        """
        Verifica si un estudiante existe en la API de estudiantes
        Implementa fail-fast para garantizar integridad de datos
        """
        try:
            response = await self._make_request_with_retry(
                "GET", 
                f"{self.base_url}/estudiantes/{id_estudiante}"
            )
            return response.status_code == 200
            
        except HTTPException:
            # Re-lanzar errores HTTP (503, etc.)
            raise
        except Exception as e:
            # Para otros errores, fallar explícitamente
            raise HTTPException(
                status_code=503,
                detail=f"No se pudo verificar la existencia del estudiante {id_estudiante}: {str(e)}"
            )
    
    async def close(self):
        """
        Cierra el cliente HTTP
        """
        await self.client.aclose()

# Instancia singleton del cliente
estudiantes_client = EstudiantesClient()
