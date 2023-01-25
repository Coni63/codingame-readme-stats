from __future__ import annotations

from dataclasses import dataclass
from dataclasses_json import dataclass_json

from domain.interfaces.i_profile import IValue
from domain.interfaces.i_user_info import IUserDto
from domain.interfaces.i_language import ILanguageDto
from domain.interfaces.i_certification import ICertificationDto
from domain.interfaces.i_achievement import IAchievementDto
from domain.interfaces.i_ranking import IRankingDto
from domain.interfaces.i_leaderboard import ILeaderboardDto

from domain.evaluator import get_points_from_rank, get_color

from config import constants


@dataclass_json
@dataclass
class IDataDto:
    user: IUserDto
    languages: list[ILanguageDto]
    certifications: list[ICertificationDto]
    achievements: list[IAchievementDto]
    rankings: IRankingDto
    leaderboard: ILeaderboardDto

    def get_main_level(self) -> tuple[str, str, float, str]:
        main_color, grade, score = self.leaderboard.get_main_color_and_grade()
        back_color = constants.BACK_COLOR[main_color]
        return (main_color, back_color, score, grade)

    def get_score_level(self) -> IValue:
        """
        Return the IValue representing the score based on the player's level
        """
        thresholds = [9, 16, 24, 31]
        return IValue(
            value=self.user.get_level(),
            color=get_color(self.user.get_level(), thresholds, ascending=True),
            title="Level",
            icon=constants.SVG_LEVEL,
            from_CG=False
        )

    def get_score_certificate(self) -> list[IValue]:
        """
        Return the IValue list representing the certification with the score
        """
        ans = [IValue(
            value="Wood", 
            color=constants.COLOR_WOOD, 
            title=title,
            icon=icon,
            from_CG=True
        ) for title, icon in ICertificationDto.get_titles_icon_in_order()]

        for certification in self.certifications:
            idx = certification.get_index()
            ans[idx] = IValue(
                value=certification.get_level(), 
                color=certification.get_color(),
                title=certification.get_title(),
                icon=certification.get_icon(),
                from_CG=True
            )
        return ans

    def get_score_best_language(self) -> IValue:
        """
        Return the IValue representing the score based on the number of puzzle solved in the most commnly user language
        """
        # filter added for profiles like:
        # https://www.codingame.com/profile/0bea6253b3749971f42264b5a9f61c47439016
        # profile Top 133 but everything is missing
        thresholds = [10, 25, 50, 100]

        if len(self.languages) == 0:  
            return IValue(
                value="N/A", 
                color=constants.COLOR_WOOD,
                title="Best Language",
                icon=constants.SVG_BEST_LANGUAGE,
                from_CG=False
            )

        top = max(self.languages, key=lambda x: x.puzzleCount)
        return IValue(
            value=top.languageName, 
            color=get_color(top.puzzleCount, thresholds, ascending=True),
            title="Best Language",
            icon=constants.SVG_BEST_LANGUAGE,
            from_CG=False
        )

    def get_score_total_solved(self) -> IValue:
        """
        Return the IValue representing the score based on the number of puzzle solved
        """
        thresholds = [25, 50, 125, 250]
        total = sum(x.puzzleCount for x in self.languages)
        return IValue(
            value=total, 
            color=get_color(total, thresholds, ascending=True),
            title="Puzzles Solved",
            icon=constants.SVG_PUZZLE_SOLVED,
            from_CG=False
        )

    def get_score_list_language(self) -> list[IValue]:
        """
        Return the IValue representing the score based on the number of puzzle solvd by language
        """
        thresholds = [10, 25, 50, 100]
        svgs = [
            constants.SVG_TOP_1, 
            constants.SVG_TOP_2, 
            constants.SVG_TOP_3, 
            constants.SVG_TOP_4, 
            constants.SVG_TOP_5, 
            constants.SVG_TOP_6
        ]
        top = sorted(self.languages, key=lambda x: x.puzzleCount, reverse=True)
        return [IValue(
            value=f"{lang.puzzleCount} puzzles" if lang.puzzleCount > 1 else "1 puzzle", 
            color=get_color(lang.puzzleCount, thresholds, ascending=True),
            title=lang.languageName,
            icon=svg,
            from_CG=False
        ) for svg, lang in zip(svgs, top)]

    def get_score_achievements(self) -> IValue:
        """
        Return the IValue representing the score based on the player's success and rareness of each of them
        """
        # Based on points given to every success (harder succes provides more points)
        # the sum of achieved success / total success is used
        # threshold used are 67% of the remaining players at every steps
        # To be a legend, you need to have 80% of success score
        # every success does not count
        # [1-((0.67)**i) for i in range(1, 5)]
        thresholds = [0.33, 0.55, 0.70, 0.79]

        total_solved = 0
        total_available = 0
        count_solved = 0
        count_available = 0
        for achievement in self.achievements:
            if not achievement.can_count():
                continue

            solved, weight = achievement.get_weight()
            if solved:
                total_solved += weight
                count_solved += 1

            total_available += weight
            count_available += 1

        return IValue(
            color=get_color(total_solved / total_available, thresholds, ascending=True),
            title="Success",
            icon=constants.SVG_SUCCESS,
            from_CG=False,
            numerator=count_solved,
            denominator=count_available,
        )

    def get_score_rank(self) -> IValue:
        """
        Return the IValue representing the score based on the player's current ranking in the global leaderboard
        """
        # threshold used are 25% of the remaining players at every steps limited to 100k
        # wood is bottom 75%
        # bronze is bottom 75% for the 25% remaining players
        # and so forth
        # Silver is top 6.25%
        # Gold is top 1.56%
        # Legend is 0.4% top players
        # [100000*((0.25)**i) for i in range(1, 5)]
        thresholds = [390, 1562, 6250, 25000]

        rank = self.user.codingamer.rank
        last_rank = self.user.codingamePointsRankingDto.numberCodingamersGlobal

        return IValue(
            color=get_color(rank, thresholds, ascending=False),
            title="Global Rank",
            icon=constants.SVG_GLOBAL_RANK,
            from_CG=False,
            numerator=rank,
            denominator=last_rank,
        )

    def get_score_competition(self, online=False):
        """
        Return the IValue representing the score based on the player best result in online or offline bot battle
        """
        # threshold used are 60% of the remaining players at every steps limited to 100k
        # wood is bottom 60%
        # bronze is bottom 60% for the 40% remaining players
        # and so forth
        # Silver is top 16%
        # Gold is top 6.5%
        # Legend is 1.5% top players
        # everything is based on 5000 base score from CG's formula
        # [math.pow(5000, (2000-((0.4**i)*2000)+1)/2000) for i in range(1, 5)]
        thresholds = [166, 1285, 2911, 4037]

        if online:
            if len(self.rankings.challenges) == 0:
                return IValue(
                    value="N/A", 
                    color=constants.COLOR_WOOD,
                    title="Highest Compet.",
                    icon=constants.SVG_HIGHEST_COMP,
                    from_CG=False
                )

            top = max(self.rankings.challenges, key=lambda x: get_points_from_rank(x.ranking, x.total))

            points = get_points_from_rank(top.ranking, top.total)
            return IValue(
                color=get_color(points, thresholds, ascending=True),
                title="Highest Compet.",
                icon=constants.SVG_HIGHEST_COMP,
                from_CG=False,
                numerator=top.ranking,
                denominator=top.total,
            )
        else:
            f = [x for x in self.rankings.puzzles if x.puzzleType == "BOT_PROGRAMMING"]

            if len(f) == 0:
                return IValue(
                    value="N/A", 
                    color=constants.COLOR_WOOD,
                    title="Highest Compet.",
                    icon=constants.SVG_HIGHEST_COMP,
                    from_CG=False
                )

            top = max(f, key=lambda x: x.points)
            return IValue(
                color=get_color(top.points, thresholds, ascending=True),
                title="Highest Compet.",
                icon=constants.SVG_HIGHEST_COMP,
                from_CG=False,
                numerator=top.ranking,
                denominator=top.totalPlayers,
            )

    def get_score_list_leaderboard(self) -> list[IValue]:
        """
        Return the IValue for each subrank on the leaderboard
        """
        val_global = IValue(
            value=None, 
            color=self.leaderboard.get_color_for("global"),
            title="Global",
            icon=constants.SVG_GLOBAL_RANK,
            from_CG=False,
            numerator=self.leaderboard.globalPointsRankGlobal,
            denominator=self.leaderboard.totalCodingamerGlobal.global_
        )
        val_challenge = IValue(
            value=None, 
            color=self.leaderboard.get_color_for("contest"),
            title="Competition",
            icon=constants.SVG_CONTEST,
            from_CG=False,
            numerator=self.leaderboard.contestPointsRankGlobal,
            denominator=self.leaderboard.totalCodingamerGlobal.contest
        )
        val_bot_prog = IValue(
            value=None, 
            color=self.leaderboard.get_color_for("bot"),
            title="AI battle",
            icon=constants.SVG_AI_BATTLE,
            from_CG=False,
            numerator=self.leaderboard.botProgrammingPointsRankGlobal,
            denominator=self.leaderboard.totalCodingamerGlobal.botProgramming
        )
        val_clash = IValue(
            value=None, 
            color=self.leaderboard.get_color_for("clash"),
            title="Clashs",
            icon=constants.SVG_CLASH,
            from_CG=False,
            numerator=self.leaderboard.clashPointsRankGlobal,
            denominator=self.leaderboard.totalCodingamerGlobal.clash
        )
        val_optim = IValue(
            value=None, 
            color=self.leaderboard.get_color_for("optim"),
            title="Optimization",
            icon=constants.SVG_OPTIM,
            from_CG=False,
            numerator=self.leaderboard.optimPointsRankGlobal,
            denominator=self.leaderboard.totalCodingamerGlobal.optim
        )
        val_codegolf = IValue(
            value=None, 
            color=self.leaderboard.get_color_for("codegolf"),
            title="Codegolf",
            icon=constants.SVG_CODEGOLF,
            from_CG=False,
            numerator=self.leaderboard.codegolfPointsRankGlobal,
            denominator=self.leaderboard.totalCodingamerGlobal.codegolf
        )

        return [val_global, val_challenge, val_bot_prog, val_optim, val_clash, val_codegolf]
