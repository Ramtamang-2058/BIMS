from django.urls import path, include

from rest_framework import routers
from .views import (TeamLeadsView,
                    TeamMembersView,
                    TeamView,
                    OrganizationView,
                    TeamLeadsNepaliView,
                    TeamMembersNepaliView,
                    OrganizationNepaliView,
                    HospitalEnglishView,
                    HospitalNepaliView,
                    EquipmentEnglishView,
                    EquipmentNepaliView,
                    ResourceEnglishNewsView,
                    ResourceEnglishAnnouncementView,
                    ResourceEnglishVideoView,
                    ResourceEnglishArticleView,
                    ResourceAnnouncementNepaliView,
                    ResourceNepaliNewsView,
                    ResourceNepaliVideoView,
                    ResourceNepaliArticleView,
                    AchievementNepaliView,
                    AchievementEnglishView,
                    SolveEnglishView,
                    SolveNepaliView,
                    DiscussionView,
                    CommentAndVoteView,
                    HelpRequestView,
                    LiveHelpRequestForOxygenCylinderView,
                    LiveHelpRequestForOxygenVentilatorView,
                    LiveHelpRequestForOxygenPlantView,
                    LiveHelpRequestForDialysisMachineView,
                    LiveHelpRequestForOtherView,
                    CommunityBoardOfDirectorEnglishView,
                    CommunityTechnicalTeamEnglishView,
                    CommunityAdvisoryCommittteeEnglishView,
                    CommunityManagementCommitteeEnglishView,
                    CommunityBoardOfDirectorNepaliView,
                    CommunityTechnicalTeamNepaliView,
                    CommunityAdvisoryCommittteeNepaliView,
                    CommunityManagementCommitteeNepaliView,
                    HitCountView,
                     )

route = routers.DefaultRouter()
route.register('post_members', TeamView, basename='postmember')
route.register('get_team_leads/en', TeamLeadsView, basename='getteamlead')
route.register('get_team_members/en', TeamMembersView, basename='getteammember')
route.register('get_organization/en', OrganizationView, basename='getorganization')
route.register('get_team_leads/np', TeamLeadsNepaliView, basename='getteamleadsnepali')
route.register('get_team_members/np', TeamMembersNepaliView, basename='getteammebernepali')
route.register('get_organization/np', OrganizationNepaliView, basename='getorganizationnepali')
route.register('hospital/en', HospitalEnglishView, basename='hospitalenglish')
route.register('hospital/np', HospitalNepaliView, basename='hospitalnepali')
# route.register('hospitalinfo/en', HospitalInfoView, basename='hospitalinfo')
route.register('equipment/en', EquipmentEnglishView, basename='equipmentenglish')
route.register('equipment/np', EquipmentNepaliView, basename='equipmentnepali')
route.register('resource/news/en', ResourceEnglishNewsView, basename='newsenglish')
route.register('resource/video/en', ResourceEnglishVideoView, basename='videoenglish')
route.register('resource/articles/en', ResourceEnglishArticleView, basename='articleenglish')
route.register('resource/announcement/en', ResourceEnglishAnnouncementView, basename='announcementenglish')
route.register('resource/announcement/np', ResourceAnnouncementNepaliView, basename='resourcepostandgetinnepali')
route.register('resource/news/np', ResourceNepaliNewsView, basename='newsnepali')
route.register('resource/video/np', ResourceNepaliVideoView, basename='videoinnepali')
route.register('resource/articles/np', ResourceNepaliArticleView, basename='articleview')
route.register('achievement/np', AchievementNepaliView, basename='achivementnepali')
route.register('achievement/en', AchievementEnglishView)
route.register('solve/en', SolveEnglishView, basename='solveenglish')
route.register('solve/np', SolveNepaliView)
route.register('discussion', DiscussionView)
route.register('comment_and_like', CommentAndVoteView)
route.register('request_for_help', HelpRequestView, basename='requestforhelp')
route.register('live_request/oxygen_cylinder', LiveHelpRequestForOxygenCylinderView, basename='OCliverequest')
route.register('live_request/oxygen_ventilator', LiveHelpRequestForOxygenVentilatorView, basename='OVliverequest')
route.register('live_request/oxygen_plant', LiveHelpRequestForOxygenPlantView, basename='OPliverequest')
route.register('live_request/dialysis_machine', LiveHelpRequestForDialysisMachineView, basename='DMliverequest')
route.register('live_request/others', LiveHelpRequestForOtherView, basename='othersliverequest')
route.register('mot/boardofdirector/en', CommunityBoardOfDirectorEnglishView, basename='boardofdirectors')
route.register('mot/technicalteam/en', CommunityTechnicalTeamEnglishView, basename='technicalteam')
route.register('mot/advisorycommittee/en', CommunityAdvisoryCommittteeEnglishView, basename='advisorycommitee')
route.register('mot/managmentcommittee/en', CommunityManagementCommitteeEnglishView, basename='managementcommitee')
route.register('mot/boardofdirector/np', CommunityBoardOfDirectorNepaliView, basename='communityboardofdirector')
route.register('mot/technicalteam/np', CommunityTechnicalTeamNepaliView, basename='technicalteam')
route.register('mot/advisorycommittee/np', CommunityAdvisoryCommittteeNepaliView, basename='advisorycommittee')
route.register('mot/managmentcommittee/np', CommunityManagementCommitteeNepaliView, basename='managementcommittee')
route.register('visitors', HitCountView)

urlpatterns = [
    path('api/', include(route.urls)),
]