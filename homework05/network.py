import typing as tp
from collections import defaultdict

import community as community_louvain
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

from friends import get_friends, get_mutual


def ego_network(
        user_id: tp.Optional[int] = None, friends: tp.Optional[tp.List[int]] = None
) -> tp.List[tp.Tuple[int, int]]:
    """
    Построить эгоцентричный граф друзей.

    :param user_id: Идентификатор пользователя, для которого строится граф друзей.
    :param friends: Идентификаторы друзей, между которыми устанавливаются связи.
    :return: Список ребер (связей) между друзьями.
    """
    # Получаем список друзей, если они не переданы в функцию
    if friends is None:
        friends_response = get_friends(user_id)
        friends = [friend["id"] for friend in friends_response.items]

    # Собираем список ребер между друзьями
    edges = []
    for i, friend in enumerate(friends):
        mutual_friends = get_mutual(source_uid=friend, target_uids=friends[i + 1:])
        for mutual_friend in mutual_friends:
            edges.append((friend, mutual_friend))

    return edges


def plot_ego_network(net: tp.List[tp.Tuple[int, int]], with_labels: bool = True) -> None:
    """
    Отрисовать эгоцентричный граф друзей.

    :param net: Граф, созданный с помощью функции ego_network.
    :param with_labels: Наносить или нет на граф имена пользователей.
    """
    graph = nx.Graph()
    graph.add_edges_from(net)

    # Настраиваем расположение узлов
    layout = nx.spring_layout(graph)

    # Отрисовка графа
    nx.draw(graph, layout, node_size=10, node_color="black", alpha=0.5, with_labels=with_labels, font_size=8)
    plt.title("Ego Network", size=15)
    plt.show()


def plot_communities(net: tp.List[tp.Tuple[int, int]]) -> None:
    """
    Отрисовать эгоцентричный граф друзей с выделением сообществ.

    :param net: Граф, созданный с помощью функции ego_network.
    """
    graph = nx.Graph()
    graph.add_edges_from(net)

    # Рассчитываем сообщества с помощью алгоритма Лувена
    partition = community_louvain.best_partition(graph)

    # Настраиваем расположение узлов
    layout = nx.spring_layout(graph)

    # Отрисовываем граф, цвет узлов соответствует их сообществу
    nx.draw(graph, layout, node_size=25, node_color=list(partition.values()), alpha=0.8, cmap=plt.cm.rainbow)
    plt.title("Ego Network with Communities", size=15)
    plt.show()


def get_communities(net: tp.List[tp.Tuple[int, int]]) -> tp.Dict[int, tp.List[int]]:
    """
    Выделить сообщества в эго-сети.

    :param net: Граф, созданный с помощью функции ego_network.
    :return: Словарь, где ключ — номер сообщества, а значение — список ID пользователей в этом сообществе.
    """
    communities = defaultdict(list)
    graph = nx.Graph()
    graph.add_edges_from(net)

    # Алгоритм Лувена для обнаружения сообществ
    partition = community_louvain.best_partition(graph)

    for uid, cluster in partition.items():
        communities[cluster].append(uid)

    return communities


def describe_communities(
        clusters: tp.Dict[int, tp.List[int]],
        friends: tp.List[tp.Dict[str, tp.Any]],
        fields: tp.Optional[tp.List[str]] = None,
) -> pd.DataFrame:
    """
    Описать сообщества друзей.

    :param clusters: Словарь сообществ {номер сообщества: [список друзей]}.
    :param friends: Список друзей с расширенной информацией.
    :param fields: Поля, которые необходимо включить в описание.
    :return: DataFrame с описанием сообществ.
    """
    if fields is None:
        fields = ["first_name", "last_name"]

    data = []
    for cluster_n, cluster_users in clusters.items():
        for uid in cluster_users:
            for friend in friends:
                if uid == friend["id"]:
                    data.append([cluster_n] + [friend.get(field) for field in fields])
                    break

    return pd.DataFrame(data=data, columns=["cluster"] + fields)
