#!/bin/bash

# Docker Image Filesystem Extractor
# Usage: ./extract_docker_images.sh [source_folder] [output_folder]

set -e  # Exit on any error

# Default directories
SOURCE_DIR="${1:-./docker_images}"
OUTPUT_DIR="${2:-./extracted_containers}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}[EXTRACT]${NC} $1"
}

# Check if source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    print_error "Source directory '$SOURCE_DIR' does not exist!"
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Function to extract a single Docker image
extract_docker_image() {
    local tar_file="$1"
    local base_name=$(basename "$tar_file" .tar)
    local extract_dir="$OUTPUT_DIR/$base_name"
    local temp_dir=$(mktemp -d)
    
    print_header "Processing: $base_name"
    
    # Create extraction directory
    mkdir -p "$extract_dir"
    
    # Extract the tar file to temp directory
    print_status "Extracting tar file..."
    tar -xf "$tar_file" -C "$temp_dir" 2>/dev/null || {
        print_error "Failed to extract $tar_file"
        rm -rf "$temp_dir"
        return 1
    }
    
    # Find and extract layer tarballs
    local layer_count=0
    local filesystem_dir="$extract_dir/filesystem"
    mkdir -p "$filesystem_dir"
    
    print_status "Extracting Docker layers..."
    
    # Look for layer.tar files or *.tar files in subdirectories
    find "$temp_dir" -name "layer.tar" -o -name "*.tar" | while read layer_tar; do
        # Skip the main tar file we already extracted
        if [ "$layer_tar" != "$tar_file" ]; then
            layer_count=$((layer_count + 1))
            print_status "  Extracting layer $layer_count..."
            tar -xf "$layer_tar" -C "$filesystem_dir" 2>/dev/null || {
                print_warning "Could not extract layer: $layer_tar"
            }
        fi
    done
    
    # Also try extracting any .tar.gz files
    find "$temp_dir" -name "*.tar.gz" | while read layer_tar; do
        layer_count=$((layer_count + 1))
        print_status "  Extracting compressed layer $layer_count..."
        tar -xzf "$layer_tar" -C "$filesystem_dir" 2>/dev/null || {
            print_warning "Could not extract compressed layer: $layer_tar"
        }
    done
    
    # Copy manifest and config files if they exist
    find "$temp_dir" -name "manifest.json" -exec cp {} "$extract_dir/" \; 2>/dev/null || true
    find "$temp_dir" -name "*.json" -exec cp {} "$extract_dir/" \; 2>/dev/null || true
    find "$temp_dir" -name "repositories" -exec cp {} "$extract_dir/" \; 2>/dev/null || true
    
    # Create a summary file
    cat > "$extract_dir/extraction_info.txt" << EOF
Docker Image: $base_name
Source: $tar_file
Extracted: $(date)
Filesystem Location: $filesystem_dir

Contents:
$(ls -la "$extract_dir" 2>/dev/null || echo "Could not list contents")

Filesystem Root:
$(ls -la "$filesystem_dir" 2>/dev/null || echo "No filesystem extracted")
EOF
    
    # Clean up temp directory
    rm -rf "$temp_dir"
    
    # Check if extraction was successful
    if [ -d "$filesystem_dir" ] && [ "$(ls -A "$filesystem_dir" 2>/dev/null)" ]; then
        print_status "Successfully extracted to: $extract_dir"
        print_status "Filesystem available at: $filesystem_dir"
    else
        print_warning "Extraction completed but no filesystem found for $base_name"
    fi
    
    echo ""
}

# Main execution
print_status "Docker Image Filesystem Extractor"
print_status "Source directory: $SOURCE_DIR"
print_status "Output directory: $OUTPUT_DIR"
echo ""

# Count tar files
tar_count=$(find "$SOURCE_DIR" -name "*.tar" -type f | wc -l)
print_status "Found $tar_count tar files to process"
echo ""

if [ $tar_count -eq 0 ]; then
    print_warning "No .tar files found in $SOURCE_DIR"
    exit 0
fi

# Process each tar file
processed=0
failed=0

find "$SOURCE_DIR" -name "*.tar" -type f | while read tar_file; do
    if extract_docker_image "$tar_file"; then
        processed=$((processed + 1))
    else
        failed=$((failed + 1))
    fi
done

# Final summary
echo ""
print_status "Extraction complete!"
print_status "Check the extracted filesystems in: $OUTPUT_DIR"
print_status "Each container's filesystem is in: [container_name]/filesystem/"

# Create a browse script
cat > "$OUTPUT_DIR/browse_containers.sh" << 'EOF'
#!/bin/bash
# Quick browser for extracted containers

EXTRACT_DIR="$(dirname "$0")"

echo "Available extracted containers:"
echo "================================"

for dir in "$EXTRACT_DIR"/*/; do
    if [ -d "$dir" ]; then
        container_name=$(basename "$dir")
        filesystem_path="$dir/filesystem"
        
        echo "Container: $container_name"
        if [ -d "$filesystem_path" ]; then
            echo "  Filesystem: $filesystem_path"
            echo "  Root contents: $(ls "$filesystem_path" 2>/dev/null | head -10 | tr '\n' ' ')"
        else
            echo "  No filesystem directory found"
        fi
        echo ""
    fi
done

echo ""
echo "To explore a container filesystem:"
echo "  cd $EXTRACT_DIR/[container_name]/filesystem"
echo "  ls -la"
echo ""
echo "To view extraction info:"
echo "  cat $EXTRACT_DIR/[container_name]/extraction_info.txt"
EOF

chmod +x "$OUTPUT_DIR/browse_containers.sh"

print_status "Created browse script: $OUTPUT_DIR/browse_containers.sh"
print_status "Run it to see all extracted containers!"