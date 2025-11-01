import asyncio
import logging
from aiohttp import web
from config import HEALTH_CHECK_PORT

logger = logging.getLogger(__name__)

class HealthCheckServer:
    def __init__(self):
        self.app = web.Application()
        self.app.router.add_get('/', self.health_check)
        self.app.router.add_get('/health', self.health_check)
        self.runner = None
        self.site = None
    
    async def health_check(self, request):
        return web.Response(text='OK', status=200)
    
    async def start(self):
        try:
            self.runner = web.AppRunner(self.app)
            await self.runner.setup()
            self.site = web.TCPSite(self.runner, '0.0.0.0', HEALTH_CHECK_PORT)
            await self.site.start()
            logger.info(f"Health check server started on port {HEALTH_CHECK_PORT}")
        except Exception as e:
            logger.error(f"Error starting health check server: {e}")
    
    async def stop(self):
        try:
            if self.site:
                await self.site.stop()
            if self.runner:
                await self.runner.cleanup()
            logger.info("Health check server stopped")
        except Exception as e:
            logger.error(f"Error stopping health check server: {e}")
