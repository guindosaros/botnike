import argparse



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", required=True)
    
    args = parser.parse_args()
    
    print(f'Hello world {args.username}')