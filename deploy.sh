#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Print header
echo -e "${GREEN}=======================================================${NC}"
echo -e "${GREEN}            Microservices Deployment Script            ${NC}"
echo -e "${GREEN}=======================================================${NC}"

# Function to display usage
usage() {
    echo -e "\nUsage:"
    echo -e "  ${CYAN}./deploy.sh [options]${NC}"
    echo -e "\nOptions:"
    echo -e "  ${CYAN}-h, --help${NC}      Show this help message"
    echo -e "  ${CYAN}-t, --type${NC}      Deployment type (helm or k8s)"
    echo -e "\nExamples:"
    echo -e "  ${CYAN}./deploy.sh --type helm${NC}    # Deploy using Helm"
    echo -e "  ${CYAN}./deploy.sh --type k8s${NC}     # Deploy using plain Kubernetes manifests"
    echo -e "  ${CYAN}./deploy.sh${NC}               # Will prompt for deployment type\n"
}

# Parse command line arguments
DEPLOYMENT_TYPE=""
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -t|--type)
            DEPLOYMENT_TYPE="$2"
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            usage
            exit 1
            ;;
    esac
done

# Validate the script is run from the project root
if [ ! -d "scripts" ] || [ ! -f "scripts/setup-cluster.sh" ]; then
    echo -e "${RED}Error: This script must be run from the project root directory${NC}"
    echo -e "${RED}Please cd to the root of the microservices-python project${NC}"
    exit 1
fi

# If deployment type is not provided, ask user
if [ -z "$DEPLOYMENT_TYPE" ]; then
    echo -e "\n${YELLOW}Choose deployment method:${NC}"
    echo -e "  1) ${CYAN}Helm${NC} - Deploy using Helm charts"
    echo -e "  2) ${CYAN}Kubernetes${NC} - Deploy using plain Kubernetes manifests"
    read -p "Enter your choice (1 or 2): " CHOICE
    
    case $CHOICE in
        1)
            DEPLOYMENT_TYPE="helm"
            ;;
        2)
            DEPLOYMENT_TYPE="k8s"
            ;;
        *)
            echo -e "${RED}Invalid choice. Exiting.${NC}"
            exit 1
            ;;
    esac
fi

# Setup the cluster
echo -e "\n${YELLOW}Step 1: Setting up the KIND-CLUSTER...${NC}"
bash ./scripts/setup-cluster.sh

# Execute the appropriate deployment script
echo -e "\n${YELLOW}Step 2: Deploying services using ${DEPLOYMENT_TYPE}...${NC}"
if [ "$DEPLOYMENT_TYPE" = "helm" ]; then
    bash ./scripts/deploy-helm.sh
elif [ "$DEPLOYMENT_TYPE" = "k8s" ]; then
    bash ./scripts/deploy-k8s.sh
else
    echo -e "${RED}Error: Invalid deployment type: $DEPLOYMENT_TYPE${NC}"
    echo -e "${RED}Valid options are 'helm' or 'k8s'${NC}"
    usage
    exit 1
fi


