#!/usr/bin/env python3
"""
Docker Registry Clone Script
Clones entire Docker images from a registry using only Python.
Creates docker-load compatible tarballs for each tag.
"""

import asyncio
import aiofiles
import tarfile
import tempfile
import pathlib
import argparse
import json
import sys
import logging
from typing import List, Dict, Any, Optional, Tuple
import aiohttp
from urllib.parse import urlparse, urljoin
import base64

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Constants
DEFAULT_REGISTRY = "https://registry.example.com"
TARGET_PLATFORM = ("linux", "amd64")
VERIFY_TLS = False
DEFAULT_PAGE_SIZE = 100


class DockerRegistryClient:
    """
    Simple Docker Registry HTTP API v2 client using aiohttp directly.
    """
    
    def __init__(self, registry_url: str, verify_ssl: bool = True):
        self.registry_url = registry_url.rstrip('/')
        self.verify_ssl = verify_ssl
        self.session = None
        
    async def __aenter__(self):
        connector = aiohttp.TCPConnector(verify_ssl=self.verify_ssl)
        self.session = aiohttp.ClientSession(connector=connector)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def _request(self, method: str, path: str, **kwargs) -> aiohttp.ClientResponse:
        """Make a request to the registry API."""
        url = urljoin(self.registry_url, path)
        
        # Add default headers
        headers = kwargs.pop('headers', {})
        if 'Accept' not in headers:
            headers['Accept'] = 'application/json'
            
        response = await self.session.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()
        return response


async def list_repositories(client: DockerRegistryClient, page_size: int = DEFAULT_PAGE_SIZE) -> List[str]:
    """
    List all repositories in the registry with pagination support.
    """
    repositories = []
    url = "/v2/_catalog"
    params = {"n": page_size}
    
    while True:
        try:
            response = await client._request("GET", url, params=params)
            data = await response.json()
            
            if "repositories" in data and data["repositories"]:
                repositories.extend(data["repositories"])
                logger.info(f"Found {len(data['repositories'])} repositories (total: {len(repositories)})")
            
            # Check for pagination
            link_header = response.headers.get("Link")
            if link_header and 'rel="next"' in link_header:
                # Extract next URL from Link header
                # Format: </v2/_catalog?n=100&last=repo>; rel="next"
                next_url = None
                for part in link_header.split(","):
                    if 'rel="next"' in part:
                        next_url = part.split(";")[0].strip("<> ")
                        break
                
                if next_url:
                    url = next_url
                    params = {}  # URL already contains params
                else:
                    break
            else:
                break
                
        except aiohttp.ClientResponseError as e:
            logger.error(f"Failed to list repositories: HTTP {e.status}")
            if e.status >= 400:
                break
            break
        except Exception as e:
            logger.error(f"Error listing repositories: {e}")
            break
    
    return repositories


async def get_tags(client: DockerRegistryClient, repo: str, page_size: int = DEFAULT_PAGE_SIZE) -> List[str]:
    """
    Get all tags for a repository with pagination support.
    """
    tags = []
    url = f"/v2/{repo}/tags/list"
    params = {"n": page_size}
    
    while True:
        try:
            response = await client._request("GET", url, params=params)
            data = await response.json()
            
            if "tags" in data and data["tags"]:
                tags.extend(data["tags"])
                logger.info(f"Found {len(data['tags'])} tags (total: {len(tags)})")
            
            # Check for pagination
            link_header = response.headers.get("Link")
            if link_header and 'rel="next"' in link_header:
                # Extract next URL from Link header
                # Format: </v2/repo/tags/list?n=100&last=tag>; rel="next"
                next_url = None
                for part in link_header.split(","):
                    if 'rel="next"' in part:
                        next_url = part.split(";")[0].strip("<> ")
                        break
                
                if next_url:
                    url = next_url
                    params = {}  # URL already contains params
                else:
                    break
            else:
                break
                
        except aiohttp.ClientResponseError as e:
            logger.error(f"Failed to get tags: HTTP {e.status}")
            if e.status >= 400:
                continue
            break
        except Exception as e:
            logger.error(f"Error getting tags: {e}")
            break
    
    return tags


async def fetch_manifest(client: DockerRegistryClient, repo: str, tag: str) -> Optional[Dict[str, Any]]:
    """
    Fetch and parse manifest, handling both manifest lists and image manifests.
    Returns the amd64 manifest or None if not found.
    """
    try:
        # Get manifest with both possible media types
        headers = {
            "Accept": "application/vnd.docker.distribution.manifest.list.v2+json, "
                     "application/vnd.docker.distribution.manifest.v2+json, "
                     "application/vnd.oci.image.manifest.v1+json"
        }
        
        response = await client._request("GET", f"/v2/{repo}/manifests/{tag}", headers=headers)
        manifest = await response.json()
        
        media_type = manifest.get("mediaType", "")
        
        # Handle manifest list (multi-architecture)
        if "manifest.list" in media_type or manifest.get("manifests"):
            logger.info(f"Found manifest list for {repo}:{tag}")
            manifests = manifest.get("manifests", [])
            
            # List all available platforms
            platforms = [(m.get("platform", {}).get("os", "unknown"), 
                         m.get("platform", {}).get("architecture", "unknown")) 
                        for m in manifests]
            logger.info(f"Available platforms: {platforms}")
            
            # Find amd64 manifest
            for m in manifests:
                platform = m.get("platform", {})
                if (platform.get("os") == TARGET_PLATFORM[0] and 
                    platform.get("architecture") == TARGET_PLATFORM[1]):
                    # Fetch the actual manifest
                    digest = m["digest"]
                    logger.info(f"Fetching {TARGET_PLATFORM[0]}/{TARGET_PLATFORM[1]} manifest: {digest}")
                    response = await client._request("GET", f"/v2/{repo}/manifests/{digest}")
                    return await response.json()
            
            logger.warning(f"No {TARGET_PLATFORM[0]}/{TARGET_PLATFORM[1]} manifest found for {repo}:{tag}")
            return None
        
        # Single architecture manifest
        logger.info(f"Found single manifest for {repo}:{tag}")
        return manifest
        
    except aiohttp.ClientResponseError as e:
        logger.error(f"Failed to fetch manifest for {repo}:{tag}: HTTP {e.status}")
        return None
    except Exception as e:
        logger.error(f"Error fetching manifest for {repo}:{tag}: {e}")
        return None


async def download_blob(client: DockerRegistryClient, repo: str, digest: str, out_dir: pathlib.Path) -> Optional[pathlib.Path]:
    """
    Download a blob to the output directory.
    """
    try:
        # Clean digest for filename (remove sha256: prefix)
        clean_digest = digest.replace("sha256:", "")
        output_path = out_dir / f"{clean_digest}.tar.gz"
        
        # Skip if already exists
        if output_path.exists():
            logger.info(f"Blob already exists: {clean_digest[:12]}...")
            return output_path
        
        logger.info(f"Downloading blob: {clean_digest[:12]}...")
        
        response = await client._request("GET", f"/v2/{repo}/blobs/{digest}")
        
        async with aiofiles.open(output_path, "wb") as f:
            async for chunk in response.content.iter_chunked(8192):
                await f.write(chunk)
        
        logger.info(f"Downloaded blob: {clean_digest[:12]}... ({output_path.stat().st_size} bytes)")
        return output_path
        
    except aiohttp.ClientResponseError as e:
        logger.error(f"Failed to download blob {digest[:12]}...: HTTP {e.status}")
        return None
    except Exception as e:
        logger.error(f"Error downloading blob {digest[:12]}...: {e}")
        return None


def create_docker_load_tarball(manifest: Dict[str, Any], config_path: pathlib.Path, 
                              layer_paths: List[pathlib.Path], output_path: pathlib.Path, 
                              repo: str, tag: str) -> bool:
    """
    Create a Docker-compatible tarball that can be loaded with 'docker load'.
    """
    try:
        with tarfile.open(output_path, "w") as tar:
            temp_dir = pathlib.Path(tempfile.mkdtemp())
            
            try:
                # Create manifest.json for docker load
                config_digest = manifest["config"]["digest"].replace("sha256:", "")
                layer_digests = [layer["digest"].replace("sha256:", "") for layer in manifest["layers"]]
                
                docker_manifest = [{
                    "Config": f"{config_digest}.json",
                    "RepoTags": [f"{repo}:{tag}"],
                    "Layers": [f"{digest}.tar.gz" for digest in layer_digests]
                }]
                
                manifest_json = temp_dir / "manifest.json"
                with open(manifest_json, "w") as f:
                    json.dump(docker_manifest, f)
                tar.add(manifest_json, arcname="manifest.json")
                
                # Add config file
                config_json = temp_dir / f"{config_digest}.json"
                config_json.write_bytes(config_path.read_bytes())
                tar.add(config_json, arcname=f"{config_digest}.json")
                
                # Add layer files
                for layer_path in layer_paths:
                    if layer_path and layer_path.exists():
                        tar.add(layer_path, arcname=layer_path.name)
                
                logger.info(f"Created tarball: {output_path}")
                return True
                
            finally:
                # Cleanup temp directory
                import shutil
                shutil.rmtree(temp_dir, ignore_errors=True)
                
    except Exception as e:
        logger.error(f"Error creating tarball: {e}")
        return False


async def list_all_repositories(registry_url: str, page_size: int = DEFAULT_PAGE_SIZE, 
                               quiet: bool = False) -> bool:
    """
    List all repositories in the registry.
    """
    if quiet:
        logging.getLogger().setLevel(logging.WARNING)
    
    async with DockerRegistryClient(registry_url, verify_ssl=VERIFY_TLS) as client:
        logger.info(f"Listing repositories from: {registry_url}")
        repositories = await list_repositories(client, page_size)
        
        if not repositories:
            logger.warning("No repositories found")
            return False
        
        logger.info(f"\n=== Found {len(repositories)} repositories ===")
        for repo in sorted(repositories):
            print(repo)
        
        return True


async def download_all_repositories(registry_url: str, output_dir: pathlib.Path,
                                   page_size: int = DEFAULT_PAGE_SIZE, quiet: bool = False) -> bool:
    """
    Download all repositories from the registry.
    """
    if quiet:
        logging.getLogger().setLevel(logging.WARNING)
    
    total_repos = 0
    success_repos = 0
    total_tags = 0
    success_tags = 0
    
    async with DockerRegistryClient(registry_url, verify_ssl=VERIFY_TLS) as client:
        logger.info(f"Discovering all repositories from: {registry_url}")
        repositories = await list_repositories(client, page_size)
        
        if not repositories:
            logger.warning("No repositories found")
            return False
        
        total_repos = len(repositories)
        logger.info(f"Found {total_repos} repositories to download")
        
        # Process each repository
        for i, repo in enumerate(repositories, 1):
            logger.info(f"\n=== Repository {i}/{total_repos}: {repo} ===")
            
            try:
                # Get all tags for this repository
                tags = await get_tags(client, repo, page_size)
                
                if not tags:
                    logger.warning(f"No tags found for {repo}, skipping...")
                    continue
                
                repo_success = 0
                total_tags += len(tags)
                logger.info(f"Found {len(tags)} tags: {', '.join(tags)}")
                
                # Process each tag
                for tag in tags:
                    logger.info(f"Processing {repo}:{tag}")
                    
                    # Fetch manifest
                    manifest = await fetch_manifest(client, repo, tag)
                    if not manifest:
                        logger.warning(f"Skipping {repo}:{tag} - no suitable manifest")
                        continue
                    
                    # Create temporary directory for this tag
                    with tempfile.TemporaryDirectory() as temp_dir:
                        temp_path = pathlib.Path(temp_dir)
                        
                        # Download config blob
                        config_digest = manifest["config"]["digest"]
                        config_path = await download_blob(client, repo, config_digest, temp_path)
                        
                        if not config_path:
                            logger.error(f"Failed to download config for {repo}:{tag}")
                            continue
                        
                        # Download layer blobs
                        layers = manifest.get("layers", [])
                        
                        layer_paths = []
                        for j, layer in enumerate(layers):
                            layer_digest = layer["digest"]
                            logger.info(f"Layer {j+1}/{len(layers)}: {layer_digest[:12]}...")
                            layer_path = await download_blob(client, repo, layer_digest, temp_path)
                            layer_paths.append(layer_path)
                        
                        # Filter out failed downloads
                        valid_layer_paths = [p for p in layer_paths if p is not None]
                        
                        if len(valid_layer_paths) != len(layers):
                            logger.warning(f"Only {len(valid_layer_paths)}/{len(layers)} layers downloaded")
                        
                        # Create output tarball
                        output_file = output_dir / f"{repo.replace('/', '_')}_{tag}.tar"
                        success = create_docker_load_tarball(manifest, config_path, valid_layer_paths, 
                                                           output_file, repo, tag)
                        
                        if success:
                            repo_success += 1
                            success_tags += 1
                            logger.info(f"Successfully created: {output_file}")
                        else:
                            logger.error(f"Failed to create tarball for {repo}:{tag}")
                
                if repo_success > 0:
                    success_repos += 1
                    logger.info(f"Repository {repo}: {repo_success}/{len(tags)} tags successful")
                else:
                    logger.error(f"Repository {repo}: No tags downloaded successfully")
                    
            except Exception as e:
                logger.error(f"Error processing repository {repo}: {e}")
                continue
    
    logger.info(f"\n=== Download All Summary ===")
    logger.info(f"Repositories processed: {success_repos}/{total_repos}")
    logger.info(f"Tags downloaded: {success_tags}/{total_tags}")
    logger.info(f"Output directory: {output_dir}")
    
    return success_repos > 0


async def clone_repository(registry_url: str, repo: str, output_dir: pathlib.Path, 
                          page_size: int = DEFAULT_PAGE_SIZE, quiet: bool = False) -> bool:
    """
    Clone entire repository with all tags.
    """
    if quiet:
        logging.getLogger().setLevel(logging.WARNING)
    
    success_count = 0
    
    async with DockerRegistryClient(registry_url, verify_ssl=VERIFY_TLS) as client:
        # Get all tags
        logger.info(f"Fetching tags for repository: {repo}")
        tags = await get_tags(client, repo, page_size)
        
        if not tags:
            logger.error("No tags found")
            return False
        
        logger.info(f"Found {len(tags)} tags: {', '.join(tags)}")
        
        # Process each tag
        for tag in tags:
            logger.info(f"\n=== Processing {repo}:{tag} ===")
            
            # Fetch manifest
            manifest = await fetch_manifest(client, repo, tag)
            if not manifest:
                logger.warning(f"Skipping {repo}:{tag} - no suitable manifest")
                continue
            
            # Create temporary directory for this tag
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = pathlib.Path(temp_dir)
                
                # Download config blob
                config_digest = manifest["config"]["digest"]
                logger.info(f"Downloading config: {config_digest[:12]}...")
                config_path = await download_blob(client, repo, config_digest, temp_path)
                
                if not config_path:
                    logger.error(f"Failed to download config for {repo}:{tag}")
                    continue
                
                # Download layer blobs
                layers = manifest.get("layers", [])
                logger.info(f"Downloading {len(layers)} layers...")
                
                layer_paths = []
                for i, layer in enumerate(layers):
                    layer_digest = layer["digest"]
                    logger.info(f"Layer {i+1}/{len(layers)}: {layer_digest[:12]}...")
                    layer_path = await download_blob(client, repo, layer_digest, temp_path)
                    layer_paths.append(layer_path)
                
                # Filter out failed downloads
                valid_layer_paths = [p for p in layer_paths if p is not None]
                
                if len(valid_layer_paths) != len(layers):
                    logger.warning(f"Only {len(valid_layer_paths)}/{len(layers)} layers downloaded successfully")
                
                # Create output tarball
                output_file = output_dir / f"{repo.replace('/', '_')}_{tag}.tar"
                success = create_docker_load_tarball(manifest, config_path, valid_layer_paths, 
                                                   output_file, repo, tag)
                
                if success:
                    success_count += 1
                    logger.info(f"Successfully created: {output_file}")
                else:
                    logger.error(f"Failed to create tarball for {repo}:{tag}")
    
    logger.info(f"\n=== Summary ===")
    logger.info(f"Successfully processed: {success_count}/{len(tags)} tags")
    return success_count > 0


def main():
    parser = argparse.ArgumentParser(
        description="Clone Docker images from registry using only Python",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s myapp
  %(prog)s --registry https://my-registry.com myapp
  %(prog)s --output ./images --quiet myapp
  %(prog)s --list --registry https://my-registry.com
  %(prog)s --download-all --registry https://my-registry.com --output ./backup
        """
    )
    
    parser.add_argument("repository", nargs="?", help="Repository name (e.g., 'library/nginx')")
    parser.add_argument("--registry", default=DEFAULT_REGISTRY, 
                       help=f"Registry URL (default: {DEFAULT_REGISTRY})")
    parser.add_argument("--output", type=pathlib.Path, default=pathlib.Path("."),
                       help="Output directory (default: current directory)")
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE,
                       help=f"Pagination size for tag listing (default: {DEFAULT_PAGE_SIZE})")
    parser.add_argument("--quiet", action="store_true",
                       help="Suppress progress output")
    parser.add_argument("--list", action="store_true",
                       help="List all repositories in the registry")
    parser.add_argument("--download-all", action="store_true",
                       help="Download all repositories and tags from the registry")
    
    args = parser.parse_args()
    
    # Handle --download-all command
    if args.download_all:
        # Create output directory
        args.output.mkdir(parents=True, exist_ok=True)
        
        try:
            success = asyncio.run(download_all_repositories(
                args.registry, args.output, args.page_size, args.quiet
            ))
            sys.exit(0 if success else 1)
        except KeyboardInterrupt:
            logger.info("Interrupted by user")
            sys.exit(2)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            sys.exit(3)
    
    # Handle --list command
    if args.list:
        try:
            success = asyncio.run(list_all_repositories(
                args.registry, args.page_size, args.quiet
            ))
            sys.exit(0 if success else 1)
        except KeyboardInterrupt:
            logger.info("Interrupted by user")
            sys.exit(2)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            sys.exit(3)
    
    # Repository is required for cloning
    if not args.repository:
        parser.error("repository argument is required when not using --list or --download-all")
    
    # Create output directory
    args.output.mkdir(parents=True, exist_ok=True)
    
    # Run the async clone function
    try:
        success = asyncio.run(clone_repository(
            args.registry, args.repository, args.output, args.page_size, args.quiet
        ))
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        sys.exit(2)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(3)


if __name__ == "__main__":
    main()