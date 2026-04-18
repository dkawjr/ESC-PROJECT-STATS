import pandas as pd

from nows_esc.scales import add_domain_scores


def test_domain_scores_sum_items() -> None:
    row = {
        "Pre Simulation Knowledge: Question 5": 1,
        "Pre Simulation Knowledge: Question 6": 1,
        "Pre Simulation Knowledge: Question 7": 0,
        "Pre Simulation Knowledge: Question 8": 1,
        "Pre Simulation Knowledge: Question 9": 1,
        "Post Simulation Knowledge: Question 5": 1,
        "Post Simulation Knowledge: Question 6": 1,
        "Post Simulation Knowledge: Question 7": 1,
        "Post Simulation Knowledge: Question 8": 1,
        "Post Simulation Knowledge: Question 9 ": 1,
        "Pre Simulation Comfort: 11a": 1,
        "Pre Simulation Comfort: 11b": 2,
        "Pre Simulation Comfort: 11c": 3,
        "Pre Simulation Comfort: 11d": 4,
        "Post Simulation Comfort: 10a": 2,
        "Post Simulation Comfort: 10b": 3,
        "Post Simulation Comfort: 10c": 4,
        "Post Simulation Comfort: 10d": 5,
        "Pre Simulation Attitude: 12a__rev": 5,
        "Pre Simulation Attitude: 12b__rev": 4,
        "Pre Simulation Attitude: 12c__rev": 3,
        "Pre Simulation Attitude: 12d__rev": 2,
        "Pre Simulation Attitude: 12e__rev": 1,
        "Post Simulation Attitude: 11a__rev": 5,
        "Post Simulation Attitude: 11b__rev": 5,
        "Post Simulation Attitude: 11c__rev": 5,
        "Post Simulation Attitude: 11d__rev": 5,
        "Post Simulation Attitude: 11e__rev": 5,
    }
    df = pd.DataFrame([row])
    out = add_domain_scores(df)
    assert out.loc[0, "knowledge_pre_total"] == 4
    assert out.loc[0, "knowledge_post_total"] == 5
    assert out.loc[0, "comfort_pre_total"] == 10
    assert out.loc[0, "comfort_post_total"] == 14
    assert out.loc[0, "attitude_pre_total"] == 15
    assert out.loc[0, "attitude_post_total"] == 25
