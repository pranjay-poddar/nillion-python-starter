from nada_dsl import *

def secure_voting():
    party1 = Party(name="Party1")
    party2 = Party(name="Party2")

    party1_vote = SecretInteger(Input(name="party1_vote", party=party1))
    party2_vote = SecretInteger(Input(name="party2_vote", party=party2))

    decrypted_vote1 = party1.decrypt(party1_vote)
    decrypted_vote2 = party2.decrypt(party2_vote)

    total_votes = decrypted_vote1 + decrypted_vote2

    winner = If(total_votes > PublicInteger(50), "Party1 Wins!", "Party2 Wins!")

    out1 = Output(decrypted_vote1, "Decrypted Vote Party1", party1)
    out2 = Output(decrypted_vote2, "Decrypted Vote Party2", party2)
    out3 = Output(winner, "Election Winner", party1)

    return [out1, out2, out3]

secure_voting()
