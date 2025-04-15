from pipeline_core.utils.utils import load_flow_inputs, load_yaml, patch_openai_logging

patch_openai_logging()


from dotenv import load_dotenv

load_dotenv()


# pipeline_core/flows/run_flow.py
if __name__ == "__main__":
    import argparse
    import asyncio

    from pipeline_core.models.models import PromptFlowRunner
    from pipeline_core.utils.utils import load_yaml

    parser = argparse.ArgumentParser()
    parser.add_argument("--flow", required=True, help="Path to the YAML flow file")
    args = parser.parse_args()

    flow_config = load_yaml(args.flow)  # ✅ this returns a dict
    initial_input = load_flow_inputs(flow_config)

    runner = PromptFlowRunner(flow_config)  # ✅ passes dict to the runner
    output = asyncio.run(runner.run(initial_input))
    print("✅ Flow finished. Final output:")
    print(output)
