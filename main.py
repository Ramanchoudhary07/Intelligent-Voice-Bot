"""
Main entry point for the Intelligent Voice Bot
"""
import argparse
import sys
from pathlib import Path
from src.voice_bot import VoiceBot
from src.analytics import Analytics
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Intelligent Voice Bot")
    parser.add_argument(
        "--audio",
        type=str,
        help="Path to audio file to process"
    )
    parser.add_argument(
        "--text",
        type=str,
        help="Text query to process (for testing)"
    )
    parser.add_argument(
        "--analytics",
        action="store_true",
        help="Show analytics summary"
    )
    
    args = parser.parse_args()
    
    # Initialize Voice Bot
    try:
        bot = VoiceBot()
    except Exception as e:
        logger.error(f"Failed to initialize Voice Bot: {str(e)}")
        sys.exit(1)
    
    # Process audio file
    if args.audio:
        audio_path = Path(args.audio)
        if not audio_path.exists():
            logger.error(f"Audio file not found: {args.audio}")
            sys.exit(1)
        
        logger.info(f"Processing audio file: {args.audio}")
        output_file = bot.process_audio_file(str(audio_path))
        
        if output_file:
            logger.info(f"Response audio saved to: {output_file}")
        else:
            logger.error("Failed to process audio file")
            sys.exit(1)
    
    # Process text query
    elif args.text:
        logger.info(f"Processing text query: {args.text}")
        response_text, audio_file = bot.process_text_query(args.text)
        
        # print(f"\nResponse: {response_text}")
        if audio_file:
            print(f"Audio saved to: {audio_file}")
    
    # Show analytics
    elif args.analytics:
        analytics = Analytics()
        summary = analytics.get_summary()
        
        print("\n=== Analytics Summary ===")
        for key, value in summary.items():
            print(f"{key}: {value}")
    
    else:
        # Interactive mode
        print("\n=== Intelligent Voice Bot ===")
        print("Enter text queries (or 'exit' to quit, 'analytics' for stats):\n")
        
        while True:
            try:
                query = input("You: ").strip()
                
                if query.lower() in ["exit", "quit", "q"]:
                    print("Goodbye!")
                    break
                
                if query.lower() == "analytics":
                    analytics = Analytics()
                    summary = analytics.get_summary()
                    print("\n=== Analytics Summary ===")
                    for key, value in summary.items():
                        print(f"{key}: {value}")
                    print()
                    continue
                
                if not query:
                    continue
                
                response_text, audio_file = bot.process_text_query(query)
                print(f"Bot: {response_text}")
                
                if audio_file:
                    print(f"(Audio response saved to: {audio_file})\n")
            
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                logger.error(f"Error in interactive mode: {str(e)}")


if __name__ == "__main__":
    main()

