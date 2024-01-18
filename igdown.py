import instaloader
import os
import argparse
import shutil

def download_images(username, download_folder):
    L = instaloader.Instaloader()

    try:
        # Load profile by username
        profile = instaloader.Profile.from_username(L.context, username)

        # Create the download folder if it doesn't exist
        os.makedirs(download_folder, exist_ok=True)

        # Download each image
        for post in profile.get_posts():
            if post.is_video or post.typename == 'GraphSidecar':  # Skip videos and albums
                continue

            image_url = post.url
            image_filename = os.path.join(download_folder, f"{post.date_utc.strftime('%Y-%m-%d_%H-%M-%S')}.jpg")

            # Check if the file already exists or if it has an unwanted extension
            unwanted_extensions = ['.json.xz', '.txt']
            if not os.path.exists(image_filename) and not any(image_filename.lower().endswith(ext) for ext in unwanted_extensions):
                # Download image
                L.download_post(post, target=download_folder)
                print(f"Image downloaded: {image_filename}")

    except instaloader.exceptions.InstaloaderException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Instagram Image Downloader")
    parser.add_argument("-u", "--username", required=True, help="Instagram profile username")
    parser.add_argument("-o", "--output", required=True, help="Download folder path")

    args = parser.parse_args()
    username = args.username
    download_folder = args.output

    download_images(username, download_folder)

    # Masuk ke download_folder
    os.chdir(download_folder)

    # Menghapus berkas dengan ekstensi .json.xz dan .txt
    unwanted_extensions = ['.json.xz', '.txt']
    for file_name in os.listdir():
        if any(file_name.lower().endswith(ext) for ext in unwanted_extensions):
            os.remove(file_name)

    print("Cleanup completed.")
