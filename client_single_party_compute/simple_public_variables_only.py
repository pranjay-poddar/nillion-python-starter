from pdb import set_trace as bp
import argparse
import asyncio
import py_nillion_client as nillion
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from helpers.nillion_client_helper import create_nillion_client

load_dotenv()

# 1 Party running compute with only public variables
async def main():
    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    userkey_path = os.getenv("NILLION_WRITERKEY_PATH")
    userkey = nillion.UserKey.from_file(userkey_path)
    client = create_nillion_client(userkey)
    party_id = client.party_id()
    user_id = client.user_id()

    program_id=f"{user_id}/simple_public_variables_only"
    party_name="Party1"


    # Bind the parties in the computation to the client to set input and output parties
    compute_bindings = nillion.ProgramBindings(program_id)
    compute_bindings.add_input_party(party_name, party_id)
    compute_bindings.add_output_party(party_name, party_id)

    print(f"Computing using program {program_id}")

    public_variables = nillion.PublicVariables({
        "A": nillion.PublicVariableInteger(10),
        "B": nillion.PublicVariableInteger(6),
    })
    
    # Compute on the secrets
    compute_id = await client.compute(
        cluster_id,
        compute_bindings,
        [],
        nillion.Secrets({}),
        public_variables,
    )

    # Print compute result
    print(f"The computation was sent to the network. compute_id: {compute_id}")
    while True:
        compute_event = await client.next_compute_event()
        if isinstance(compute_event, nillion.ComputeFinishedEvent):
            print(f"✅  Compute complete for compute_id {compute_event.uuid}")
            print(f"🖥️  The result is {compute_event.result.value}")
            break
    



    

asyncio.run(main())