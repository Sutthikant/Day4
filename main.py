import os
import asyncio
import aiohttp
import aiofiles
from bs4 import BeautifulSoup
import time

class ImageData:
    def __init__(self, title, img_url):
         self.name = title
         self.img_url = img_url

async def download_and_save(img_url, filename, session):
    async with session.get(img_url) as response:
        picture = await response.read()
        # print(picture)
        async with aiofiles.open(filename, mode='wb') as f:
            await f.write(picture)

async def scrape(url, session):
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.text()
                # print(data)
        
        soup = BeautifulSoup(data, 'html.parser')

        images = []

        image_blocks = soup.find_all('li', {'class': 'gallerybox'})

        count = 0
        max_images = 100

        for block in image_blocks:
                count += 1
                if count > max_images:
                    break

                imgs = block.find_all('img')
                if len(imgs) > 0:
                    img_url = imgs[0]['src']

                    header = block.find('div', {'class': 'gallerytext'})
                    link = header.find('a')
                    title = link.text
                    images.append(ImageData(title, img_url))

        if not os.path.exists('images'):
                os.makedirs('images')
        
        # print(images)

        download_coroutine = []

        # for image in images:
        #     await download_and_save(image.img_url, f'images/{image.name}', session)
            
        for image in images:
            download_coroutine.append(download_and_save(image.img_url, f'images/{image.name}', session))
        
        await asyncio.gather(*download_coroutine)

async def main():
    async with aiohttp.ClientSession() as session:
        await scrape('https://commons.wikimedia.org/wiki/Category:Pictures_of_the_day_(2023)', session)

if __name__ == '__main__':
    start = time.time()
    asyncio.run(main())
    stop = time.time()
    diff = stop - start
    print(f"Time taken: {diff} seconds")